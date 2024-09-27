const fileInput = document.getElementById('file-upload')
const previewContainer = document.getElementById('preview-container')
const previewImage = document.getElementById('preview-image')




fileInput.addEventListener('change', function() {
    const file = this.files[0]
    if (file) {
        const reader = new FileReader()

        reader.addEventListener('load', function() {
            previewImage.setAttribute('src', this.result)
            previewContainer.style.display = 'flex'
        });

        reader.readAsDataURL(file)
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function toggleLikeImage(id,author) {

    const imgElement = document.getElementById('like-icon-'+id);

    const img1 = "/static/img/icons8-love-24%20(1).png";
    const img2 = "/static/img/icons8-love-24%20(2).png";

    if (imgElement.src.includes('/static/img/icons8-love-24%20(2).png')) {
        const formData = new FormData();
        formData.append('author', author);
        formData.append('post', id);


         
        fetch('/add-item/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });

        imgElement.src = img1;
    } else {
 

        fetch(`/delete-item/${context=id+','+author}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if (response.status === 204) {
                console.log('Item deleted successfully');
            } else {
                console.error('Failed to delete item');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
        imgElement.src = img2;
    }
}

open=document.getElementById("open")
close=document.getElementById("close")



open.addEventListener("click", function(event) {
    document.querySelector('.modal').style.display = 'block';
})

close.addEventListener("click", function(event) {
    document.querySelector('.modal').style.display = 'none';
})