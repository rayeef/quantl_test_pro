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

  $.HSCore.components.HSTagsInput = {
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

      return this.initInputs().data('tagify');
    },

    initInputs: function () {
      //Variables
      var $self = this,
        config = $self.config,
        collection = $self.pageCollection;

      //Actions
      return this.collection.each(function (i, el) {
        //Variables
        var $this = $(el),
          clearBtn = $this.data('clear-btn'),
          listManual = Boolean($this.data('list-manual'));

        $this.tagify(config);

        var tagify = $this.data('tagify');

        // Remove all button
        $(clearBtn).on("click", tagify.removeAllTags.bind(tagify));

        // List manual
        if (listManual) {
          renderSuggestionsList();
        }

        function renderSuggestionsList(){
          tagify.dropdown.show.call(tagify) // Load the list
          $this.parent()[0].appendChild(tagify.DOM.dropdown)
        }

        //Actions
        collection = collection.add($this);
      });
    }
  };
})(jQuery);
