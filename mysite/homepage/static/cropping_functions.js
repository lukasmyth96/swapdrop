function triggerImageUpload(btn) {
    // Trigger click on hidden file upload button
    const targetElementFieldName = btn.id.split('_').pop()  // e.g. 'image', 'image2' etc.
    const targetIdToClick = 'id_' + targetElementFieldName  // id of the hidden upload button
    document.getElementById(targetIdToClick).click()  // click the hidden upload button
}

function readFileAsync(file) {
    // This function returns a Promise with resolve value as a base64 encoding of the uploading image
    // We do this so we can display the uploaded image in the cropper
    return new Promise((resolve, reject) => {
        let reader = new FileReader();

        reader.onload = () => {
            resolve(reader.result);
        };

        reader.onerror = reject;

        reader.readAsDataURL(file);
    })
}


async function processFile(event) {
    // Converts uploaded file to base64 and starts a croppie with that image src
    const targetElementFieldName = event.target.id.split('_').pop()  // e.g. 'image', 'image2' etc.
    $('#upload_placeholder_' + targetElementFieldName).css('display', 'none');  // hide the placeholder image
    const croppieContainer = $('#croppie_container_' + targetElementFieldName)
    croppieContainer.croppie('destroy')  // destroy any existing croppies
    try {
        const file = event.target.files[0];  // get the uploaded file
        const src = await readFileAsync(file);  // read base64 str from file to display

        // Start croppie with the uploaded image src
        croppieContainer
            .css('display', 'block')  // make div container visible
            .croppie({
                viewport: {width: 150, height: 150},
                boundary: {width: 200, height: 200}
            })
            .croppie('bind', {url: src});  // display uploaded image in croppied container

    } catch (err) {
        console.log(err);
    }
}

function getCropDimensions(event) {
    const croppieContainer = event.target;
    const targetElementFieldName = croppieContainer.id.split('_').pop()  // e.g. 'image', 'image2' etc.
    const croppedDimensions = $('#croppie_container_' + targetElementFieldName).croppie('get').points.join();
    $('#crop_dimensions_' + targetElementFieldName).val(croppedDimensions);  // store value in hidden <input>
}