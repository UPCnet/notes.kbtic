$(document).ready(function () {

// Tags select2 field
$('#searchbytag').select2({
    tags: [],
    tokenSeparators: [","],
    minimumInputLength: 1,
    ajax: {
        url: portal_url + '/getVocabularies?name=plone.app.vocabularies.Keywords&field=subjects',
        data: function (term, page) {
            return {
                query: term,
                page: page // page number
            };
        },
        results: function (data, page) {
            return data;
        }
    }
});

// Tags search
$('#searchbytag').on("change", function(e) {
    var query = $('#searchinputcontent .searchInput').val();
    var path = $(this).data().name;
    var tags = $('#searchbytag').val();

    $('.listingBar').hide();
        $.get(path + '/search_filtered_content', { q: query, t: tags }, function(data) {
        $('#tagslist').html(data);
    });
});

// Content search
$('#searchinputcontent .searchInput').on('keyup', function(event) {
    var query = $(this).val();
    var path = $(this).data().name;
    var tags = $('#searchbytag').val();
    $('.listingBar').hide();
    $.get(path + '/search_filtered_content', { q: query, t: tags }, function(data) {
        $('#tagslist').html(data);
    });
});

});