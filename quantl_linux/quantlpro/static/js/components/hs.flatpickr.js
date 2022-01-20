/**
 * Range datepicker wrapper.
 *
 * @author Htmlstream
 * @version 1.0
 *
 */

var isEmpty = function isEmpty(f) {
    return (/^function[^{]+\{\s*\}/m.test(f.toString()));
  }

;(function ($) {
  'use strict';

  function get2DigitFmt(val) {
    return ('0' + val).slice(-2);
  }

  $.HSCore.components.HSFlatpickr = {
    /**
     *
     *
     * @var Object _baseConfig
     */
    _baseConfig: {
      locale: {
        firstDayOfWeek: 1,
        weekdays: {
          shorthand: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
        },
        rangeSeparator: ' - '
      },
      disable: [],
      nextArrow: '<em class="nova-arrow-right"></em>',
      prevArrow: '<em class="nova-arrow-left"></em>',
      onDayCreate: function () {}
    },

    /**
     *
     *
     * @var jQuery pageCollection
     */
    pageCollection: $(),

    /**
     * Initialization of Range datepicker wrapper.
     *
     * @param String selector (optional)
     * @param Object config (optional)
     *
     * @return jQuery pageCollection - collection of initialized items.
     */

    init: function (selector, config) {

      this.collection = selector && $(selector).length ? $(selector) : $();
      if (!$(selector).length) return;

      this.config = config && $.isPlainObject(config) ?
        $.extend({}, this._baseConfig, config) : this._baseConfig;

      this.config.itemSelector = selector;

      this.initFlatpickr();

      return this.pageCollection;

    },

    initFlatpickr: function () {
      //Variables
      var $self = this,
        config = $self.config,
        collection = $self.pageCollection;

      //Actions
      this.collection.each(function (i, el) {
        //Variables
        var $this = $(el),
          open = false,
          optWrapper = $this.data('rp-wrapper'),
          optIsInline = Boolean($this.data('rp-is-inline')),
          optIsStatic = Boolean($this.data('rp-is-static')),
          optIsWrap = Boolean($this.data('rp-is-wrap')),
          optType = $this.data('rp-type'),
          optDateFormat = $this.data('rp-date-format'),
          optDefaultDate = JSON.parse(el.getAttribute('data-rp-default-date')),
          arrEventDays = JSON.parse(el.getAttribute('data-rp-event-dates')),
          monthSelectorType = $this.data('month-selector-type');

        var flatpickr = $this.flatpickr({
          inline: optIsInline, // boolean
          mode: optType ? optType : 'single', // 'single', 'multiple', 'range'
          dateFormat: optDateFormat ? optDateFormat : 'd M Y',
          defaultDate: optDefaultDate,
          appendTo: $(optWrapper)[0],
          static: optIsStatic,
          wrap: optIsWrap,
          disable: config.disable,
          readonly: false,
          monthSelectorType: monthSelectorType ? monthSelectorType : "static",
          locale: {
            firstDayOfWeek: 1,
            weekdays: {
              shorthand: config.locale.weekdays.shorthand
            },
            rangeSeparator: config.locale.rangeSeparator
          },
          onClose: function (selectedDates, dateStr, instance) {
            open = false;
          },
          nextArrow: config.nextArrow,
          prevArrow: config.prevArrow,
          onDayCreate: isEmpty(config.onDayCreate) === true ? function (dObj, dStr, fp, dayElem) {
            var date = $(dayElem)[0].dateObj,
              key = date.getFullYear() + get2DigitFmt(date.getMonth() + 1) + get2DigitFmt(date.getDate());

            if ($.inArray(key, arrEventDays) !== -1) {
              dayElem.innerHTML += '<span class="badge badge-xxs badge-bordered badge-secondary position-absolute rounded-circle"></span>';
            }
          } : config.onDayCreate
        });

        //Actions
        collection = collection.add($this);

        $(flatpickr.input).click(function () {
          if (open) {
            flatpickr.close();
          } else {
            open = true;
          }
        });
      });
    }
  };
})(jQuery);
