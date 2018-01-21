$(function() {
  $('#clickme').click(function() {
       $.ajax({
       url: 'http://localhost:8000/api/lodging-offers/?format=json',
       /*csrfmiddlewaretoken: "{{ csrf_token }}",*/
       dataType: 'jsonp',
       success: function(data) {
          var items = [];

          $.each(data, function(key, val) {

            items.push('<li id="' + key + '">' + val + '</li>');

          });

          $('<ul/>', {
             'class': 'interest-list',
             html: items.join('')
          }).appendTo('body');

       },
      statusCode: {
         404: function() {
           alert('There was a problem with the server.  Try again soon!');
         }
       }
    });
  });
});
