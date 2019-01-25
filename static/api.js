var api = function (method, params) {
    params = params || {}
    var settings = {
        "method": "POST",
        "type": "POST",
        "headers": {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        "body": JSON.stringify({
            "method": method,
            "params": params
        })
    };

    return fetch('http://localhost:5000/api/', settings)
}