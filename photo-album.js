var apigClient = apigClientFactory.newClient({});

function loadPhoto(json_str) {
  console.log('json_str', json_str);
  var msg = json_str["data"]["message"];
  for (var i = 0; i < msg.length; i++){
    var file_name = msg[i]["objectKey"];
    var bucket = msg[i]["bucket"];
    if (bucket !== "photob2") {continue;};
    var label = msg[i]["labels"];
    var photoSrc = "https://" + bucket + ".s3.amazonaws.com/" + file_name;
    if(photoSrc != null){
      var newElement = 
        "<img class='img-fluid w-100' src='" + photoSrc + "' alt='Failed to open image: " + photoSrc + "'>" 
      $("#imageCol").prepend(newElement);
    }
  }
}


function submitForm(e) {
  e.preventDefault();
  $("#imageCol").empty();
  var labels = $("#labelBox").val();
  var data = {'q': labels};
  apigClient.searchGet(data, {}, {})
    .then((response) => {
        console.log("search success")
        // console.log(response)
        loadPhoto(response)
  });
  }



function upload(e) {
  e.preventDefault();
  var image = document.getElementById('images').files[0];
  // console.log(typeof image);
  var extension = image.type;
  // console.log(extension);
  // var body = {'image': image}
  // additionalParams = {
  //   headers: {'Content-Type': 'application/pdf'}
  // }
  // console.log(image)
  // apigClient.uploadPut({}, body, additionalParams)
  //   .then((response) => {console.log(response['data']['body'])});
    $.ajax({
         url: "https://bfau5ukhwa.execute-api.us-east-1.amazonaws.com/photo/upload",
         type: 'PUT',
         data: image,
         dataType: 'html',
         headers: {'Content-Type': 'multipart/form-data'},
         processData: false,
         contentType: extension,
         success: function (response) {
          alert("Upload Successful");
          console.log(response);
         },
         error: function(xhr, status, error){
          errMsg = "Failed.<br>" + xhr.responseText + "<br>" + status + "<br>" + error;
          alert("errMsg");
          }
      });
}



