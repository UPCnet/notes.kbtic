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
$('#searchinputcontent .searchInput').on('keydown', function(event) {
    if (event.keyCode == 13) {
        var query = $(this).val();
        var path = $(this).data().name;
        var tags = $('#searchbytag').val();
        var obsolete = $('#include_obsolets:checked').val();
        $('.listingBar').hide();
        $.get(path + '/search_filtered_content', { q: query, t: tags, o: obsolete }, function(data) {
            $('#tagslist').html(data);
        });
    }
});

$('#searchinputcontent #include_obsolets').click( function(event){
    
    var query = $('#searchInput').val();
    var path = $(location).attr('href');
    var tags = $('#searchbytag').val();
    var obsolete = $('#include_obsolets:checked').val();
    $('.listingBar').hide();
    $.get(path + '/search_filtered_content', { q: query, t: tags, o: obsolete }, function(data) {
        $('#tagslist').html(data);
    });
});

$("a.CatItem").on("click", function (event) { 
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();
    var category = $(this).attr("value");

    //$('#searchbytag').select2('destroy');
    if ($("#searchbytag").val() == ''){
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
    }
    else{

        var catSelect = $("#searchbytag").val().split(",");
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

                var data = [];
                
                for(var i = 0; i < catSelect.length; i++){
                    data.push({id:catSelect[i],text:catSelect[i]});
                }
                data.push({id: category, text: category});
                callback(data);

            }
        }).select2('val', []);

        var catToSearch = $("#searchbytag").val();
        $("#searchbytag").val(catToSearch).trigger("change");
    }

});

//fin
});



