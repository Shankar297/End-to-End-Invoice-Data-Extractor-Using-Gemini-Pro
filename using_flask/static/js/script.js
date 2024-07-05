document.getElementById('file').addEventListener('change', function(event) {
    var reader = new FileReader();
    reader.onload = function() {
        var output = document.getElementById('preview-image');
        output.src = reader.result;
        output.style.display = 'block';
        document.getElementById('image-preview').style.display = 'block';
    };
    reader.readAsDataURL(event.target.files[0]);
});
