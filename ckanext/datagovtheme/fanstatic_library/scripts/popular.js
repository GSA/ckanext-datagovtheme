jQuery(function ($) {

  // $.getJSON( "/datagovtheme/get-popular-count", function( data ) {
  //   console.log(data);    
  // });




  var pupolar_api = "/datagovtheme/get-popular-count";
  var pkgs = {'pkgs': collect_all_packages().join(',')};
  $.getJSON(pupolar_api, pkgs, function(data) {
    $.each( data, function( key, val ) {
      console.log(key + ": " + val['recent']);
      $("ul.dataset-list li.dataset-item h3.dataset-heading").each(function() {
        if ($(this).attr('pkg_id') == key) {
          $(this).find('span.recent-views').attr('title', val['recent']).html('<i class="fa fa-line-chart"></i> ' + val['recent'] + ' recent views');
        }
      });
    });
  });


  function collect_all_packages() {
    var pkgs = [];
    // get pkg_id from ul.dataset-list li.dataset-item h3.dataset-heading[pkg_id]
    $("ul.dataset-list li.dataset-item h3.dataset-heading").each(function() {
      pkgs.push($(this).attr('pkg_id'));
    });

    return pkgs;
  } 

  // $.getJSON( pupolar_api, {
  //   pkgs: ['a', 'b', 'c'],
  //   tagmode: "any",
  //   format: "json"
  // })
  //   .done(function( data ) {
  //     console.log("###")
  //     console.log(data)
  //     var items = [];
  //     $.each( data, function( key, val ) {
  //       items.push( "<li id='" + key + "'>" + val + "</li>" );
  //     });
  //     console.log(items)
       
  //       // $( "<img>" ).attr( "src", item.media.m ).appendTo( "#images" );
  //       // if ( i === 3 ) {
  //       //   return false;
  //       // }
  //   });
});
