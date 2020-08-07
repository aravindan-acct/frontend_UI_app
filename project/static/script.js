
    $(document).ready(()=>{

    
    $("#get_token").click(function test(){
    
    let opts = {
        redirect_uri: "http://localhost:7979/home",
        response_type: 'token',
	};
    let client = new jso.JSO({
        providerID: "petstore",
        client_id: "test",
        redirect_uri: opts, // The URL where you is redirected back, and where you perform run the callback() function.
        authorization: "https://petstore.swagger.io/oauth/authorize",
        scopes: { request:  ["read:pets", "write:pets"]},
        debug: true
    });

    client.callback();
    
    let test = client.getToken(opts);
    console.log(test);

    client.getToken(opts).then((token) =>{
        console.log("The token is: ", token);
       });
    });});

    
