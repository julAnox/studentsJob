function loadImage(event) {
  var output = document.getElementById("preview");

  output.src = URL.createObjectURL(event.target.files[0]);
  output.onload = function () {
    URL.revokeObjectURL(output.src);
  };
}


const selectCountry = document.querySelector("#selectCountry")

selectCountry.addEventListener("change", checkCountry)

async function fetchData() {
  const response = await fetch("http://127.0.0.1:8000/api/countries");

  countries = await response.json();

  countries['clean_data'].forEach((element) => {
    selectCountry.insertAdjacentHTML("beforeend",
      `<option class="country" value="${Object.keys(element)}">${Object.keys(element)}</option>`
    )
  })
}

fetchData()


function checkCountry (event) {
    try {
      document.querySelector('#select-region').remove()
    } catch (i) {}
    if (event.target.value !== "-"){
    districtClass = document.querySelector('.district').style.display = 'none'
    selectedCountry = event.target.options[event.target.selectedIndex]
    regionClass = document.querySelector('.region')
    regionClass.insertAdjacentHTML("beforeend",
        `
      <select name="region" id="select-region">
        <option value="-">-</option>
      </select>
    `)
    regionClass.style.display = 'block'
    countries['clean_data'][selectedCountry.index - 1][selectedCountry.value].forEach(element =>{
      document.querySelector('#select-region').insertAdjacentHTML("beforeend", `
            <option value="${Object.keys(element)}">${Object.keys(element)}</option>
        `)
    })
    document.querySelector('#select-region').addEventListener("change", changeRegion)
    } else {
        regionClass.style.display = 'none'
        districtClass.style.display = 'none'
    }
}

function changeRegion (event) {
  try {
      document.querySelector('#select-district').remove()
    } catch (i) {}
    if (event.target.value !== "-"){
    selectedRegion = event.target.options[event.target.selectedIndex]
    districtClass = document.querySelector('.district')
    districtClass.insertAdjacentHTML("beforeend",
        `
      <select name="district" id="select-district">
        <option value="-">-</option>
      </select>
    `)
    districtClass.style.display = 'block'
      countries['clean_data'][selectedCountry.index - 1][selectedCountry.value][selectedRegion.index - 1][selectedRegion.value].forEach(element =>{
      document.querySelector('#select-district').insertAdjacentHTML("beforeend", `
            <option value="${element}">${element}</option>
        `)
    })}
    else {
        districtClass.style.display = 'none'
    }
}
