function updateImage()
{
    newImage = new Image();

    newImage.onload = function() {
        document.getElementById("stream").src = newImage.src;
    };
    newImage.onerror = function() {
        document.getElementById("stream").src =  "{{ url_for('static', filename='placeholder.jpg') }}";
    };
    newImage.src = "{{ url_for('static', filename='last_image.jpg') }}?t=" + new Date().getTime();


    setTimeout(updateImage, 500);
}