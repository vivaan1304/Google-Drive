function createElement(tagName, attri, cont){
    let tag = document.createElement(tagName);
    for(let key in attri){
        tag.setAttribute(key, attri[key])
    }    
    tag.innerHTML = cont
    return tag
}

// function to render breadcrumbs
function render_bc(){
    let d = document.getElementById("path")
    d.innerHTML=""
    let partial_path = [];
    for(let i = 0;i < currentPath.length;i ++){
        let a = createElement("button", {"style" : "background-color : cyan"}, currentPath[i])    
        d.appendChild(a)
        d.appendChild(createElement("span", null, "/"))
        partial_path.push(currentPath[i]);
    }
}

render_bc()
document.getElementById("folder-submit").addEventListener("click", e =>{
    let folderName = document.getElementById("folder-name").value
    console.log(folderName)
    $.ajax({
        type : "POST",
        url : "/createfolder",
        data: JSON.stringify({
            "new_folder" : folderName,
            "path" : currentPath
        }),
        success: (resp)=>{
            currentPath.push(resp)
            // localStorage.setItem('stored_path', currentPath)
            render_bc()
            // console.log(currentPath)
        },
        contentType: 'application/json'
    })
})




