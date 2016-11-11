$(function (){
  // Tracking
  var url = location.pathname;
  // remove any site root from url
  url = url.substring($('body').data('locale-root'), url.length);
  // trim any trailing /
  url = url.replace(/\/*$/, '');
  $('a.resource-url-analytics').click(function (e){
    var url = $(e.target).closest('a').attr('href');
    $.ajax({url : '/_tracking',
            data : {url:url, type:'resource'},
            type : 'POST',
            complete : function () {location.href = url;},
            timeout : 30});
    e.preventDefault();
  });

  $('div.btn-group a.btn.btn-primary').each(function(){
        if($(this).find('i').attr('class') == 'icon-external-link' || $(this).find('i').attr('class') == 'icon-download-alt') {
            $(this).click(function(e){
                var url = $(this).closest('a').attr('href');
                $.ajax({url : '/_tracking',
                    data : {url:url, type:'resource'},
                    type : 'POST',
                    complete : function () {location.href = url;},
                    timeout : 30});
                e.preventDefault();
            });
        }
  });
});
