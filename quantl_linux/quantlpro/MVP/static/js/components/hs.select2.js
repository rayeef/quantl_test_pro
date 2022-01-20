/**
 * Selects wrapper.
 *
 * @author Htmlstream
 * @version 1.0
 * @requires
 *
 */
;(function ($) {
  'use strict';

  function formatData(option) {
    if (!option.element) {
      return option.text;
    }

    var result = option.element.dataset.optionTemplate ? option.element.dataset.optionTemplate : '<span>' + option.text + '</span>';

    return $.parseHTML(result);
  }

  $.HSCore.components.HSSelect2 = {
    /**
     *
     *
     * @var Object _baseConfig
     */
    _baseConfig: {
      data: []
    },

    /**
     *
     *
     * @var jQuery pageCollection
     */
    pageCollection: $(),

    /**
     * Initialization of Selects wrapper.
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

      this.initSelects();

      return this.pageCollection;
    },

    initSelects: function () {
      //Variables
      var $self = this,
        config = $self.config,
        collection = $self.pageCollection;

      //Actions
      this.collection.each(function (i, el) {
        //Variables
        var $this = $(el),
          placeholder = $this.data('placeholder'),
          width = $this.data('width'),
          classes = $this.data('classes'),
          dropdownClasses = $this.data('dropdown-classes'),
          allowClear = $this.data('allow-clear'),
          allowDynamicTags = $this.data('tags'),
          isHideSearch = Boolean($this.data('is-hide-search')),
          size = $this.data('size');

        if (size === 'sm') {
          classes = classes + ' custom-select-sm';
          dropdownClasses = dropdownClasses + ' custom-select-list-sm';
        } else if (size === 'lg') {
          classes = classes + ' custom-select-lg';
          dropdownClasses = dropdownClasses + ' custom-select-list-lg';
        }

        $this.select2({
          width: width ? width : '100%',
          minimumResultsForSearch: isHideSearch ? Infinity : false,
          placeholder: placeholder ? placeholder : null,
          containerCssClass: classes,
          dropdownCssClass: dropdownClasses,
          templateResult: formatData,
          templateSelection: formatData,
          data: config.data,
          tags: allowDynamicTags ? allowDynamicTags : false,
          allowClear: allowClear ? allowClear : false,
          escapeMarkup : function(markup) { return markup; },
        });

        $('.select2-selection').removeClass('select2-selection--single').addClass('custom-select');

        //Actions
        collection = collection.add($this);
      });
    }
  };
})(jQuery);
