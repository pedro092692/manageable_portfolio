/*js portfolio app
@author Pedro bastidas <pedro092692@hotmail.com>
@https://github.com/pedro092692/manageable_portfolio

*/

function show_image(){
    const img_input = document.getElementById('photo');
    img_input.onchange = (evt) => {
        const [file] = img_input.files;
        if (file){
            document.getElementById('photo_preview').src = URL.createObjectURL(file);
        }
    }

}

show_image();