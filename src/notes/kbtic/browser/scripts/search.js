$(document).ready(function () {

// Tags select2 field
$('#searchbytag').select2({
    tags: [],
    tokenSeparators: [","],
    minimumInputLength: 2,
    ajax: {
        url: portal_url + '/getVocabulary?name=plone.app.vocabularies.Keywords&field=subjects',
        data: function (term) {
            return {
                query: term,
            };
        },
        results: function (data) {
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