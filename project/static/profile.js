
    var user = '{{ profile|tojson }}';
    var payload = $.parseJSON(user);
    console.log(payload);
    
      var firstname = payload["firstName"];
      var lastname = payload["lastName"]
      var username = payload["username"]
      var user_row = '<tr><td class="has-text-centered">'+firstname+'</td>\
        <td class="has-text-centered">'+lastname+'</td>\
        <td class="has-text-centered">'+username+'</td>\
        </tr>';
      
      $("#profiletable").append(user_row);
    
