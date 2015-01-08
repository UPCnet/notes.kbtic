$(document).ready(function () {

// Tags select2 field
$('#searchbytag').select2({
    tags: [],
    tokenSeparators: [","],
    minimumInputLength: 1,
    ajax: {
        url: portal_url + '/getVocabularies?name=plone.app.vocabularies.Keywords',
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
    var obsolete = $('#include_obsolets:checked').val();
    $('.listingBar').hide();
    $.get(path + '/search_filtered_content', { q: query, t: tags, o: obsolete}, function(data) {
        $('#tagslist').html(data);
    });
});

// Content search
$('#searchinputcontent .searchInput').on('keyup', function(event) {
    var query = $(this).val();
    var path = $(this).data().name;
    var tags = $('#searchbytag').val();
    var obsolete = $('#include_obsolets:checked').val();
    $('.listingBar').hide();
    $.get(path + '/search_filtered_content', { q: query, t: tags, o: obsolete }, function(data) {
        $('#tagslist').html(data);
    });
});

$('#searchinputcontent #include_obsolets').click( function(event){
    
    var query = $('#searchInput').val();
    var path = $(location).attr('href');
    var tags = $('#searchbytag').val();
    var obsolete = $('#include_obsolets:checked').val();
    $('.listingBar').hide();
    new_path = path.substring(0, path.length-1);
    $.get(new_path + '/search_filtered_content', { q: query, t: tags, o: obsolete }, function(data) {
        $('#tagslist').html(data);
    });
});

$("a.CatItem").on("click", function () { 
    
    var category = $(this).attr("value");

    $('#searchbytag').select2('destroy');
    $('#searchbytag').select2({
        tags: [],
        tokenSeparators: [","],
        minimumInputLength: 1,
        ajax: {
            url: portal_url + '/getVocabularies?name=plone.app.vocabularies.Keywords',
            data: function (term, page) {
                return {
                    query: term,
                    page: page // page number
                };
            },
            results: function (data, page) {
                return data;
            }
        },
        initSelection: function (element, callback) {
            callback({id: category, text: category });
        }
    }).select2('val', []);

    $("#searchbytag").val(category).trigger("change");    

});

//fin
});



