let tipos;
let aleatorio;
let error = 0;
let total = 0;
let imagenEnv = null

function marcador(){
    document.getElementById("marcador").textContent = total-error + "/" + total
}

async function buscarTipos() {
    addCargando()
    tipos = await (await fetch('http://localhost:8000/tipos')).json()
    removeCargando()
    buscarAleatorio()
}

async function buscarAleatorio() {
    addCargando()
    aleatorio = await (await fetch('http://localhost:8000/aleatorio/')).json()
    removeCargando()
    agregarPantalla(aleatorio)
}

function agregarPantalla(data) {
    
    let d = /*html*/`<div class="card" style="max-width: 25rem; width: 100%; margin: auto;">
    <img src="./${data.ruta}" class="card-img-top" alt="...">
    <div class="card-body">
        <h6 class="card-title">Selecciona la respuesta correcta</h6>
        <div class="form-check">
            <ul class="list-group">
                ${tipos.map(ele => /*html*/`<li class="list-group-item">
                        <input class="form-check-input" type="radio" name="flexRadioDefault"
                            id="${ele.nombre.split(" ").join("")}">
                        <label class="form-check-label" for="${ele.nombre.split(" ").join("")}">
                            ${ele.nombre}
                        </label>
                    </li>`).join("")
        }
            </ul>
        </div>
        <hr>
        <div style="text-align: center;" id="cont-btn">
            <button href="#" class="btn btn-primary btn-lg" onClick="validar()">Validar</button>
        </div>
    </div>
    </div>`

    document.getElementById('nav-home').innerHTML = d
}

function validar() {
    debugger
    let selected = document.querySelector("input[name=flexRadioDefault]:checked")
    if (selected != null) {
        total = total+1
        let tipoElegido = tipos.find(ele => ele.nombre === aleatorio.tipo)
        let elegir = tipoElegido.nombre.split(" ").join("")

        if (elegir !== selected.getAttribute("id")){
            selected.classList.add('error')
            error =error+1
        }

        document.getElementById(elegir).classList.add("success")
        document.getElementById('cont-btn').innerHTML = `<button href="#" class="btn btn-primary btn-lg" onClick="buscarAleatorio()">Continuar</button>`
        marcador()
    }
}

function addCargando(){
    document.getElementById('cargando').style.display='flex'
}
function removeCargando(){
    document.getElementById('cargando').style.display='none'
}

function cargaImagen(e){
    if(!(e.target.files.length > 0)) {
        return;
    }
    imagenEnv = e.target.files[0]
    let file = new FileReader()
    file.onload=()=>{
        const srcData = file.result;
        document.getElementById("enviarBtn").classList.remove("disabled")
        document.getElementById("imageView").setAttribute('src', srcData)
    }
    file.readAsDataURL(imagenEnv)
}

function enviarImagen(){
    var formdata = new FormData();
    formdata.append("file", imagenEnv);

    var requestOptions = {
    method: 'POST',
    body: formdata,
    redirect: 'follow'
    };
    addCargando()
    fetch("http://localhost:8000/upload", requestOptions)
    .then(response =>{
        removeCargando()
        return response.text()
    })
    .then(result => {
        let element = document.getElementById('alerta');
        element.style.display="block"
        let resp = `<span>${result}</span>`.split('"').join("")



        element.innerHTML=resp
        if(result === "No demente"){
            element.classList.add("alert-primary")
        }else if(result === "Demencia muy leve"){
            element.classList.add("alert-warning")
        }else{
            element.classList.add("alert-danger")
        }
        setTimeout(()=>{
            element.classList.remove("alert-primary")
            element.classList.remove("alert-warning")
            element.classList.remove("alert-danger")
            element.style.display="none"
        }, 10000)
    })
    .catch(error =>{
        removeCargando()
        console.log('error', error)
    });
}

function toggleMarcador(){
    let opacidad = document.getElementById("marcador").style.opacity
    if(opacidad === '0'){
        document.getElementById("marcador").style.opacity=1
    }else{
        document.getElementById("marcador").style.opacity=0
    }
}

buscarTipos()