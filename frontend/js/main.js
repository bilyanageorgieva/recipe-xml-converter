$('#convert-files-form').submit(function (event) {
        var formData = new FormData(this);

        $.ajax({
            type: "POST",
            enctype: "multipart/form-data",
            url: "http://127.0.0.1:8000/api/transform/",
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