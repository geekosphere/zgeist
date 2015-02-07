
var util = {
    KEY_ENTER: 13,
    KEY_UP:    38,
    KEY_DOWN:  40,

    // highlights the query within the result
    highlightQuery: function (result, query) {
        result = result.replace(new RegExp('('+query+')', 'gi'), '<strong>$1</strong>');
        return result;
    },

    sortQuery: function (list, query) {
        // TODO: the idea is to sort alphabetically and by query,
        //       but I don't know if that really makes sense
        list.sort(function (a, b) {
            if (a > b) {
                return 1;
            }
            else if (a < b) {
                return -1;
            }
            return 0;
        });
    }

};


function TagEdit() {

    // bind input events
    $('.tag-edit .tag-add input').blur(this.onInputBlur.bind(this));
    $('.tag-edit .tag-add input').keyup(this.onInputKeyUp.bind(this));
    $('.tag-edit .tag-add input').keydown(this.onInputKeyDown.bind(this));

    // load pre-existing tags from the hidden element
    this.loadTagsFromHidden();

    this.mergeTagsMarkup();

    $('.tag-edit .tag-list').show();
    $('.tag-edit input#tags').hide();
    $('.tag-edit .help-block').hide();

}

TagEdit.prototype.onInputKeyUp = function (event) {

    console.log('TagEdit.onInputKeyUp');

    var element = $('.tag-edit .tag-add input');
    var value = element.val().trim();

    // if the last character is a comma, add the entered words
    if (value[value.length - 1] == ',') {
        _.each(value.split(','), function (tag) {
            this.addTag(tag);
        }.bind(this));

        element.val('');
        this.hideSuggestions();
        this.mergeTagsMarkup();
    }

};

TagEdit.prototype.onInputKeyDown = function (event) {

    console.log("TagEdit.onInputKeyDown " + event.which);

    if (this.keySelectSuggestions(event.which)) {
        event.preventDefault();
        return;
    }

    // user typed enter
    if (event.which == 13) {
        this.addTagsFromInput();
        event.preventDefault();
    }
    else {
        clearTimeout(this.suggestionsTimeout);
        this.suggestionsTimeout = setTimeout(
                this.userInputSuggestions.bind(this), 100);
    }

};

TagEdit.prototype.onInputBlur = function (event) {

    if (this.noInputBlur) {
        this.noInputBlur = false;
        return;
    }

    this.addTagsFromInput();

};

TagEdit.prototype.addTagsFromInput = function () {

    var element = $('.tag-edit .tag-add input');

    _.each(element.val().split(','), function (tag) {
        this.addTag(tag);
    }.bind(this));
    element.val('');
    this.hideSuggestions();
    this.mergeTagsMarkup();

};

TagEdit.prototype.addTag = function (tag) {

    tag = tag.trim();
    if (tag == '') return;
    this._tags.push(tag);
    this._tagsModified = true;
    //this._tags.sort();
    this._tags = _.uniq(this._tags);

};

TagEdit.prototype.onTagRemoveClick = function (tag) {

    this._tags = _.without(this._tags, tag);
    this._tagsModified = true;
    this.mergeTagsMarkup();

};

TagEdit.prototype.loadTagsFromHidden = function () {

    var value = $('.tag-edit input#tags').val().split(',');
    
    this._tags = [];
    for (var i = 0; i < value.length; i++) {
        var tag = value[i].trim();
        if (tag != '') this._tags.push(tag);
    }
    this._tagsModified = true;

};

TagEdit.prototype.saveTagsToHidden = function () {

    $('.tag-edit input#tags').val(this._tags.join(', '));

};

TagEdit.prototype.mergeTagsMarkup = function () {

    if (!this._tagsModified) return;

    console.log('TagEdit.mergeTagsMarkup');

    var self = this;
    var element = $('.tag-edit ul.tag-list');

    // remove deleted tags
    $('li.tag', element).filter(function () {
        return !_.contains(self._tags, $('.name', this).text());
    }).remove();

    // get all currently present tags
    var present = _.map($('li.tag .name', element), function (tag) {
        return $(tag).text();
    });

    // adds new tags to the list (only the ones that are not present):
    _.each(_.difference(self._tags, present), function (tag) {

        var markup = sprintf('<li class="tag"><span class="del-tag">&#x2716;</span> ' +
                             '<span class="name">%s</span></li>', tag);

        // append the tag markup to the list
        if ($('li.tag', element).length > 0) {
            $('li.tag', element).last().after(markup);
        }
        else {
            $(element).prepend(markup);
        }

        // attach a event listener to the delete symbol (cross)
        // for the last added tag list element:
        var added = $('li.tag', element).last();
        $('.del-tag', added).click(function (event) {
            var name = $(this).next().text();
            self.onTagRemoveClick(name);
        });

    });

    // sync markup with hidden tag input text field
    this.saveTagsToHidden();

    this._tagsModified = false;

};

/**
 * Updates the suggestions when the input changed.
 */
TagEdit.prototype.userInputSuggestions = function () {

    var element = $('.tag-edit .tag-suggestions');
    var input = $('.tag-edit .tag-add input');
    var value = input.val().trim();

    console.log('TagEdit.userInputSuggestions ('+value.length+')');
    if (value.length > 2) {
        // ...
        this.searchSuggestions(value, function (emptyResult) {
            console.log('searchSuggestions: ' + emptyResult);
            if (!emptyResult) {
                this.repositionSuggestions();
                element.show();
            }
            else {
                this.hideSuggestions();
            }
        }.bind(this));
    }
    else {
        this.hideSuggestions();
    }

};

TagEdit.prototype.searchSuggestions = function (query, callback) {

    var self = this;
    var element = $('.tag-edit .tag-suggestions');

    $(element).mouseenter(function (event) {
        self.noInputBlur = true;
    }).mouseleave(function (event) {
        self.noInputBlur = false;
    });

    $.get('/tag/suggest?q=' + encodeURIComponent(query), function (resp) {
        var tags = resp.tags;
        util.sortQuery(tags, query);
        self.keySelectedSuggestion = -1;

        $('ul', element).html( 
          _.map(tags, function (tag) {
            var caption = util.highlightQuery(tag, query);
            return sprintf('<li data-name="%s">%s</li>', tag, caption)
          }).join('\n')
        );

        $('li', element).click(function (event) {
            self.selectSuggestion($(this).data('name'));
            event.preventDefaults();
        });

        callback(tags.length == 0);
    }.bind(this));

};

TagEdit.prototype.hideSuggestions = function () {

    console.log('TagEdit.hideSuggestions');
    var element = $('.tag-edit .tag-suggestions');
    element.hide();

};

/**
 * Repositions suggestions overlay near the tag input.
 */
TagEdit.prototype.repositionSuggestions = function () {

    var suggestions = $('.tag-edit .tag-suggestions');
    var input = $('.tag-edit .tag-add input');
    // input position the suggestions div is positioned underneath:
    var position = input.position();

    // TODO: place the element based on its size, the viewport and so on
    suggestions.css({
      top: position.top - suggestions.height() - 20,
      left: position.left - 15
    });

};

TagEdit.prototype.selectSuggestion = function (name) {

    console.log('TagEdit.selectSuggestion ' + name);

    var element = $('.tag-edit .tag-add input');
    this.addTag(name);
    element.val('');
    this.hideSuggestions();
    this.mergeTagsMarkup();

};

TagEdit.prototype.keyEnterSuggestion = function (key) {

    var suggestions = $('.tag-edit .tag-suggestions');
    var element = $('.tag-edit .tag-add input');
    var name = $('li.active', suggestions).data('name');

    this.addTag(name);
    element.val('');
    this.hideSuggestions();
    this.mergeTagsMarkup();

};

TagEdit.prototype.keySelectSuggestions = function (key) {

    var ret = false;
    var element = $('.tag-edit .tag-suggestions');

    if (key == util.KEY_UP) {
        if (this.keySelectedSuggestion == -1) {

            this.keySelectedSuggestion = $('li', element).length - 1;

        }
        else {

            this.keySelectedSuggestion--;
            if (this.keySelectedSuggestion < 0) {
                this.keySelectedSuggestion = $('li', element).length - 1;
            }

        }
        ret = true;
    }
    else if (key == util.KEY_DOWN) {
        if (this.keySelectedSuggestion == -1) {

            this.keySelectedSuggestion = 0;

        }
        else {

            this.keySelectedSuggestion++;
            if (this.keySelectedSuggestion >= $('li', element).length) {
                this.keySelectedSuggestion = 0;
            }

        }
        ret = true;
    }
    else if (key == util.KEY_ENTER) {
        this.keyEnterSuggestion();

        ret = true;
    }

    console.log('keySelectSuggestions: ' + this.keySelectedSuggestion);
    if (this.keySelectedSuggestion >= 0) {
        $('li', element).removeClass('active');
        $('li', element).eq(this.keySelectedSuggestion).addClass('active');
    }
    else {
        this.keySelectedSuggestion = -1;
    }

    return ret;

};


$(function () {
    if ($('.tag-edit').length > 0) {
        new TagEdit();
    }
});


