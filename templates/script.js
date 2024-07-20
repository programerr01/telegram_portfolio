function readJson() {
    fetch('data.json')
        .then(response => response.json())
        .then(data => {
            document.getElementById("custom_logo").textContent = data.name;
            document.getElementById('name').textContent = data.name;
            document.getElementById('title').textContent = data.title;
            document.getElementById('description').textContent = data.description;
            document.getElementById('contact_').href = "mailto:" +data.email;
            document.getElementById('profile_pic').src = data.profile_pic;
        })
        .catch(error => console.error('Error:', error));
}
readJson();