var logo_ =  document.getElementById("custom_logo");
var name_ = document.getElementById('name');
var title_ = document.getElementById('title');
var contact_ = document.getElementById('contact_');
var linkedin_ = document.getElementById("linkedin_")

function loadCssPage(pageName){
    var link = document.createElement('link');
    link.rel = 'stylesheet';
    link.type = 'text/css';
    link.href = 'themes/' + pageName + '.css';
    document.getElementsByTagName('HEAD')[0].appendChild(link);
}
function readJson() {
    fetch('data.json')
        .then(response => response.json())
        .then(data => {
            document.getElementsByClassName("loading")[0].style.display = "none";
            logo_.textContent = data.name;
            name_.textContent = data.name;
            title_.textContent = data.title;
            document.getElementById('description').textContent = data.description;
            contact_.href = "mailto:" +data.email;
            linkedin_.href = data.linkedin_;
            document.getElementById('profile_pic').src = data.profile_pic;
            loadCssPage(data.theme);
            document.getElementsByClassName("main_content")[0].style.display ="block";
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
readJson()