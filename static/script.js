function bt_responsive(){
    if (document.getElementById('responsive_menu').style.display == 'block'){
        document.getElementById('responsive_menu').style.display = 'none';
    }
    else{
        document.getElementById('responsive_menu').style.display = 'block';
    }
}
function val_log(){
    form = document.getElementById('log_form')
    if (form[0].value && form[1].value){
    form_data = new FormData(form)
    form_data.append('validar','login')
    fetch('/user/val',{
        method: 'POST',
        body: form_data
    })
    .then(r => {
        if(r.redirected){
            location = r.url
        }
        else{
            r = r.text()
            r.then(r => document.getElementById('error_lg').innerHTML = r) 
        }
    })}
    else{
        document.getElementById('error_lg').innerHTML = "Preencha todos os campos de login"
    }
}
function val_cad(){
    form = document.getElementById('cad_form')
    if (form[0].value && form[1].value && form[2]){
    form_data = new FormData(form)
    form_data.append('validar','cad')
    fetch('/user/val',{
        method: 'POST',
        body: form_data
    })
    .then(r => {
        if(r.redirected){
            location = r.url
        }
        else{
            r = r.json()
            r.then(r => {
                if (r.template){
                    document.body.innerHTML = r.template;
                    ufs();
                    document.getElementById("uf").addEventListener("input", municipios, false);

                }
                else{
                    document.getElementById('error_cad').innerHTML = r.alerta
                }
            }) 
        }
    })}
    else{
        document.getElementById('error_lg').innerHTML = "Preencha todos os campos de login"
    }
}
function finalizar_cad(){
    form = document.getElementById("finalizar_cad");
    form_data = new FormData(form);
    fetch('/user/end', {
        method: 'POST',
        body: form_data
    })
    .then(r => {
        if(r.redirected){
            location = r.url
        }
    })
}
function bt_log() {
    document.getElementById('cad_div').style.display = 'none';
    document.getElementById('log_div').style.display = 'block';
    document.getElementById('btcad').style.boxShadow = 'inset 0px 0px 25px rgba(0, 0, 0, 0.5)';
    document.getElementById('btlog').style.boxShadow = 'none';
    document.getElementById('btcad').style.borderRadius =  '0px 20px 0px 0px';
}
function bt_cad() {
    document.getElementById('log_div').style.display = 'none';
    document.getElementById('cad_div').style.display = 'block';
    document.getElementById('btlog').style.boxShadow = 'inset 0px 0px 25px rgba(0, 0, 0, 0.5)';
    document.getElementById('btcad').style.boxShadow = 'none';
    document.getElementById('btlog').style.borderRadius = '20px 0px 0px 0px';
} 
function ufs(){
    x = document.getElementById("ufs")
    fetch("https://servicodados.ibge.gov.br/api/v1/localidades/estados")
    .then(r =>  r.json())
    .then(r => r.forEach(i => x.appendChild(new Option(i["sigla"]))))
}
function municipios(){
    x=document.getElementById("uf")
    y=document.getElementById("municipios")
    y.innerHTML = ''
    fetch(`https://servicodados.ibge.gov.br/api/v1/localidades/estados/${x.value}/municipios`)
    .then(r =>  r.json())
    .then(r => r.forEach(i => y.appendChild(new Option(i["nome"]))))
}
function img_apresentacao(){
    input = document.getElementById('input_img')
    if (input.files[0]) {
        var file = new FileReader();
        file.onload =()=> {
            document.getElementById("img_destaque").src = file.result;
            document.getElementById("submit").style.display = "block";
            document.getElementById("div_ap").style.marginRight = 0;
        };       
        file.readAsDataURL(input.files[0]);
    }
}
function submit(){
    var form = document.querySelector("form");
    var form = new FormData(form);
    fetch('/user/img',{
        method:'POST',
        body: form
    })
    document.getElementById("submit").style.display = "none";
    document.getElementById("div_ap").style.marginRight = "auto";
}
function logout(){
    document.cookie = "login=; path=/";
    location.reload()
}
function cursos(){
    curso = document.getElementsByClassName("cursos");
    if(curso[0].style.display == "flex"){
        curso[0].style.display = "none";
        button = document.getElementsByClassName("logout");
        button[0].style.margin = "0 37% 5%"
    }
    else{
        curso[0].style.display = "flex";
        button = document.getElementsByClassName("logout");
        button[0].style.margin = "0 37%"
    };
}
function values(json){
    input = document.getElementsByTagName("input");
    input["celular"].placeholder = json["cell"];
    input["cpf"].placeholder = json["cpf"];
    input["data_n"].placeholder = json["data_n"];
    input["email"].placeholder = json["email"];
    input["municipio"].placeholder = json["municipio"];
    input["nome"].placeholder = json["nome"];
    input["nome_s"].placeholder = json["nome_s"];
    input["uf"].placeholder = json["uf"];
    input["celular"].value = json["cell"];
    input["cpf"].value = json["cpf"];
    input["data_n"].value = json["data_n"];
    input["email"].value = json["email"];
    input["municipio"].value = json["municipio"];
    input["nome"].value = json["nome"];
    input["nome_s"].value = json["nome_s"];
    input["uf"].value = json["uf"];
    cor = document.getElementsByName("cor")
    cor.forEach(i => cheked(i, json["cor"]))
    sexo = document.getElementsByName("sexo")
    sexo.forEach(i => cheked(i, json["sexo"]))
}
function cheked(i, json){
    if(i.value == json){i.checked = true}
}
function edit_perfil(){
    curso = document.getElementsByClassName("edit_perfil");
    if(curso[0].style.display == "block"){
        curso[0].style.display = "none";
        curso[1].style.display = "none";
        button = document.getElementsByClassName("logout");
        button[0].style.margin = "0 37% 7%"
    }
    else{
        fetch("/user/img")
        .then(r =>  r.json())
        .then(r => values(r))
        curso[0].style.display = "block";
        curso[1].style.display = "block";
        button = document.getElementsByClassName("logout");
        button[0].style.margin = "0 37%"
    };
}
function edit_info(){
    form = document.getElementsByClassName('editar_perfil')[1]
    form_data = new FormData(form)
    form_data.append('edit','info')
    fetch('/edit', {
        method: 'post',
        body: form_data
    })
    .then(r => {
        r.text()
        .then(r => {
            document.getElementById('error_info').innerHTML = r
        })
    })
}
