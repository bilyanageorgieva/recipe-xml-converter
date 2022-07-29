$("#convert-files-form").submit(function (event) {
    var formData = new FormData(this);
    $.ajax({
        type: "POST",
        enctype: "multipart/form-data",
        url: "/api/transform/",
        data: formData,
        processData: false,
        contentType: false,
        xhrFields: {
            responseType: "blob"
        },
        success: function (blob) {
            // generate the download url
            var URL = window.URL || window.webkitURL;
            var downloadUrl = URL.createObjectURL(blob);

            // create the download element
            var a = document.createElement("a")
            a.href = downloadUrl;
            a.download = "zipped.zip";
            document.body.appendChild(a);
            a.click();

            // cleanup
            window.URL.revokeObjectURL(downloadUrl);
            document.removeChild(a);
        },
        error: function(){
            alert("There was an error with the file upload");
        }
    });

    event.preventDefault();
});

$("#file-with-js>.file-label>.file-input").change(function (event){
    var fileNameContainer = $(this).siblings(".file-name");
    if(this.files.length === 1){
        fileNameContainer.text(this.files[0].name);
    } else if(this.files.length > 1){
        fileNameContainer.text(this.files.length + " files selected");
    }
});
