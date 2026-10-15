/*
 * Dashboard -> settings-page sync (read side).
 *
 * Ported from the Plone module's aioa_skynet_sync.js (fetchWidgetSettings /
 * applyDashboardSettings) and the Odoo module's aioa_dashboard_sync.js.
 *
 * When the "All in One Accessibility" settings form opens, this site's
 * current configuration is read from Skynet's `widget-settings` endpoint and
 * written into the form, so changes made directly on the Skynet/ADA
 * dashboard show up on this page too -- not only changes made from this form.
 *
 * The values are applied to the FORM only. Nothing is saved to the Django
 * database until the admin clicks Save (the write direction, form ->
 * Skynet, is admin.py save_model()).
 *
 * The request is made from the browser (like Plone/Odoo), so it leaves from
 * the admin's own IP instead of one server IP that Skynet could rate-limit.
 *
 * It does nothing when:
 *   - the host is local/dev (Skynet has no registration for it; an empty
 *     read would overwrite what was last saved)
 *   - the page is the load right after Save (widget-settings has no
 *     read-after-write guarantee; a stale read would undo the save)
 *   - the form shows validation errors (it holds the admin's own values)
 *   - the admin has already started editing (never overwrite unsaved edits)
 */
(function () {
  'use strict';

  var SYNC_KEY = 'aioa_last_sync_v1';
  var SYNC_TTL_MS = 60 * 1000;
  var LOCAL_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0'];

  // ---------------------------------------------------------------- helpers

  function readConfig() {
    var node = document.getElementById('aioa-config');
    if (!node) { return null; }
    try { return JSON.parse(node.textContent); } catch (e) { return null; }
  }

  function markSynced() {
    try { window.sessionStorage.setItem(SYNC_KEY, String(Date.now())); } catch (e) { /* private mode */ }
  }

  function wasSyncedRecently() {
    try {
      var raw = window.sessionStorage.getItem(SYNC_KEY);
      if (!raw) { return false; }
      var age = Date.now() - parseInt(raw, 10);
      return !isNaN(age) && age >= 0 && age <= SYNC_TTL_MS;
    } catch (e) { return false; }
  }

  function isSet(v) { return v !== undefined && v !== null && v !== ''; }
  function truthy01(v) { return v === true || v === 1 || v === '1'; }
  function toInt(v) { var n = parseInt(v, 10); return isNaN(n) ? null : n; }
  function clamp(n, lo, hi) { return Math.min(hi, Math.max(lo, n)); }
  function byId(id) { return document.getElementById(id); }

  // Programmatic 'change' so the existing admin JS (field visibility, icon
  // highlight + size previews) reacts exactly as if the admin had clicked.
  // Those handlers only toggle visibility / highlight -- they never reset
  // values -- so this is safe.
  function fireChange(node) {
    node.dispatchEvent(new Event('change', { bubbles: true }));
  }

  // ------------------------------------------------------ form-field setters

  function setText(id, value) {
    var node = byId(id);
    if (!node || !isSet(value)) { return; }
    value = String(value);
    if (node.value !== value) { node.value = value; }
  }

  function setSelect(id, value) {
    var node = byId(id);
    if (!node || !isSet(value)) { return; }
    var ok = false;
    for (var i = 0; i < node.options.length; i++) {
      if (node.options[i].value === value) { ok = true; break; }
    }
    // Unknown token: ignore rather than write a value the form can't save.
    if (ok && node.value !== value) { node.value = value; }
  }

  function setCheckbox(id, checked) {
    var node = byId(id);
    if (!node || node.checked === !!checked) { return; }
    node.checked = !!checked;
    fireChange(node);
  }

  function setRadio(name, value) {
    if (!isSet(value)) { return; }
    var radios = document.querySelectorAll('input[type="radio"][name="' + name + '"]');
    for (var i = 0; i < radios.length; i++) {
      if (radios[i].value === value) {
        if (!radios[i].checked) {
          radios[i].checked = true;
          fireChange(radios[i]);
        }
        return;
      }
    }
  }

  // ------------------------------------------------------------------ fetch

  /*
   * Same request shape as the Plone/Odoo modules: POST with a JSON body
   * {"website_url": <host>} (a GET returns an HTML error page). The real
   * payload is nested under "Data"; some deployments answer flat, so fall
   * back to the raw JSON. Resolves to null on any failure -- never throws.
   */
  async function fetchWidgetSettings(config) {
    try {
      // no-store + unique "_" so dashboard changes are never served from a
      // browser/proxy cache.
      var response = await fetch(config.widgetSettingsUrl + '?_=' + Date.now(), {
        method: 'POST',
        cache: 'no-store',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ website_url: config.domain })
      });
      if (!response.ok) {
        console.warn('AIOA: widget-settings responded', response.status);
        return null;
      }
      var json = await response.json();
      if (json && json.Data && Object.keys(json.Data).length > 0) {
        return json.Data;
      }
      return json || null;
    } catch (err) {
      console.warn('AIOA: widget-settings call failed', err);
      return null;
    }
  }

  // ------------------------------------------------------------------ apply

  /*
   * Writes the dashboard configuration into the form fields. Returns true
   * if the payload looked like a settings payload (and was applied).
   */
  function applyDashboardSettings(data) {
    if (!data || typeof data !== 'object') { return false; }
    // Not a settings payload (e.g. an error object): do nothing rather than
    // blank the form.
    if (!('widget_color_code' in data) && !('widget_icon_type' in data)) { return false; }

    var posBox = byId('id_enable_widget_icon_position');
    var sizeBox = byId('id_enable_icon_custom_size');

    // If a flag is missing from the payload keep what the form already has.
    var customPosition = isSet(data.is_widget_custom_position)
      ? truthy01(data.is_widget_custom_position) : !!(posBox && posBox.checked);
    var customSize = isSet(data.is_widget_custom_size)
      ? truthy01(data.is_widget_custom_size) : !!(sizeBox && sizeBox.checked);

    // Checkboxes first so the right group of fields is shown.
    if (isSet(data.is_widget_custom_position)) { setCheckbox('id_enable_widget_icon_position', customPosition); }
    if (isSet(data.is_widget_custom_size)) { setCheckbox('id_enable_icon_custom_size', customSize); }

    if (typeof data.widget_color_code === 'string' && data.widget_color_code.trim()) {
      setText('id_aioa_color_code', data.widget_color_code.trim().replace(/^#/, ''));
    }

    // The write side sends widget_size as 0/1; also accept the plain tokens.
    if (data.widget_size === 1 || data.widget_size === '1' || data.widget_size === 'oversize') {
      setSelect('id_aioa_size', 'oversize');
    } else if (data.widget_size === 0 || data.widget_size === '0' || data.widget_size === 'regular') {
      setSelect('id_aioa_size', 'regular');
    }

    setRadio('aioa_icon_type', data.widget_icon_type);

    if (customPosition) {
      // Same right/left and bottom/top interpretation as the Plone module
      // and admin.py save_model().
      if (isSet(data.widget_position_right) && toInt(data.widget_position_right) !== null) {
        setText('id_to_the_right_px', clamp(toInt(data.widget_position_right), 0, 250));
        setSelect('id_to_the_right', 'to_the_right');
      } else if (isSet(data.widget_position_left) && toInt(data.widget_position_left) !== null) {
        setText('id_to_the_right_px', clamp(toInt(data.widget_position_left), 0, 250));
        setSelect('id_to_the_right', 'to_the_left');
      }
      if (isSet(data.widget_position_bottom) && toInt(data.widget_position_bottom) !== null) {
        setText('id_to_the_bottom_px', clamp(toInt(data.widget_position_bottom), 0, 250));
        setSelect('id_to_the_bottom', 'to_the_bottom');
      } else if (isSet(data.widget_position_top) && toInt(data.widget_position_top) !== null) {
        setText('id_to_the_bottom_px', clamp(toInt(data.widget_position_top), 0, 250));
        setSelect('id_to_the_bottom', 'to_the_top');
      }
    } else {
      setSelect('id_aioa_place', data.widget_position);
    }

    if (customSize) {
      if (toInt(data.widget_icon_size_custom) !== null) {
        setText('id_aioa_size_value', clamp(toInt(data.widget_icon_size_custom), 20, 150));
      }
    } else {
      setRadio('aioa_icon_size', data.widget_icon_size);
    }
    return true;
  }

  // ------------------------------------------------------------------- init

  async function init() {
    var config = readConfig();
    var form = document.querySelector('#content-main form');
    if (!config || !config.domain || !config.widgetSettingsUrl || !form) { return; }

    // Stamp every submit: the server syncs the saved values to Skynet before
    // redirecting back, and the read on that next load could be stale.
    form.addEventListener('submit', markSynced);

    if (LOCAL_HOSTS.indexOf(config.domain) !== -1) { return; }
    if (wasSyncedRecently()) { return; }
    // Re-rendered after a failed validation: the form holds the admin's own
    // values, not saved ones.
    if (form.querySelector('.errorlist') || document.querySelector('.errornote')) { return; }

    // Only a real person's input counts (programmatic events are untrusted).
    var dirty = false;
    ['input', 'change'].forEach(function (type) {
      form.addEventListener(type, function (e) { if (e.isTrusted) { dirty = true; } }, true);
    });

    var data = await fetchWidgetSettings(config);
    if (!data || dirty) { return; }  // never overwrite unsaved edits
    applyDashboardSettings(data);
  }

  // Handy from the browser console while testing: AIOA_DASHBOARD.fetch()
  window.AIOA_DASHBOARD = {
    fetch: function () { var c = readConfig(); return c ? fetchWidgetSettings(c) : Promise.resolve(null); },
    apply: applyDashboardSettings
  };

  if (document.readyState !== 'loading') {
    init();
  } else {
    document.addEventListener('DOMContentLoaded', init);
  }
})();
