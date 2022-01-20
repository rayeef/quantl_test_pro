/**
 * Summernote editor wrapper.
 *
 * @author Htmlstream
 * @version 1.0
 *
 */
(function ($) {
    'use strict';

    $.HSCore.components.HSQuilljsEditor = {
        /**
         *
         *
         * @var Object _baseConfig
         */
        _baseConfig: {
            theme: 'snow',
            toolbarOptions: [
                [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                [{ 'font': ['', 'times-new-roman'] }],
                ['bold', 'italic', 'underline', 'strike'],
                ['blockquote', 'code-block'],
                [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                [{ 'color': [] }, { 'background': [] }],
                [{ 'align': [] }],
                [{'embed': 'video'}]
            ],
        },

        /**
         *
         *
         * @var jQuery pageCollection
         */
        pageCollection: $(),

        /**
         * Initialization of Summernote editor wrapper.
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

            var Font = Quill.import('formats/font');
// We do not add Aref Ruqaa since it is the default
            Font.whitelist = ['times-new-roman', 'roboto'];
            Quill.register(Font, true);


            this.initQuilljsEditor();

            return this.pageCollection;
        },

        initQuilljsEditor: function () {
            //Variables
            var $self = this,
                config = $self.config,
                collection = $self.pageCollection;

            //Actions
            this.collection.each(function (i, el) {
                //Variables
                var $this = $(el),
                    theme = !!$this.data('theme') ? $this.data('theme') : config.theme,
                    fontNames = !!$this.data('font-names') ? JSON.parse(el.getAttribute('data-font-names')) : config.fontNames;

                var quill = new Quill($this[0], {
                    theme: theme,
                    modules: {
                        toolbar: config.toolbarOptions
                    },
                });

                //Actions
                collection = collection.add($this);
            });
        },

        method: function () {
            //Variables
            var $self = this,
                newArguments = [];

            for (var i = 1; i < arguments.length; i++) {

                newArguments.push(arguments[i]);

            }

            //Actions
            $self.collection.each(function (i, el) {
                //Variables
                var $this = $(el);

                $this.summernote.apply($this, newArguments);
            });
        }

    };

})(jQuery);
