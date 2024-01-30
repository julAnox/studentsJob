var incomeSlider = document.getElementById("income");
var incomeOutput = document.getElementById("incomeValue");
incomeOutput.innerHTML = incomeSlider.value;
incomeSlider.oninput = function () {
  incomeOutput.innerHTML = this.value;
};

const selectCountry = document.querySelector('#select-country')

selectCountry.addEventListener("change", checkCountry)

async function fetchData() {
  const response = await fetch("http://127.0.0.1:8000/api/countries");

  countries = await response.json();

  console.log("Полученные данные:", countries);

  countries['clean_data'].forEach((element) => {
    selectCountry.insertAdjacentHTML("beforeend",
      `<option class="country" value="${Object.keys(element)}">${Object.keys(element)}</option>`
    )
  })
}
fetchData();

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

async function getFilters (event) {
    let data = {}

    data['country'] = '-'
    data['region'] = '-'
    data['district'] = '-'
    let selectCountryFilter = document.querySelector("#select-country")
    data['country'] = selectCountryFilter.value
    if (selectCountryFilter.value !== "-") {
        let selectRegionFilter = document.querySelector("#select-region")
        data['region'] = selectRegionFilter.value
        if (selectRegionFilter.value !== "-") {
            let selectDistrictFilter = document.querySelector("#select-district")
                data['district'] = selectDistrictFilter.value
        }
    }

    let selectExperience = document.querySelector("#select-experience")
    data['experience'] = selectExperience.value

    let incomeOutput = document.getElementById("incomeValue");
    data['income'] = incomeOutput.textContent

    let selectCurrency = document.getElementById("select-currency");
    data['currency'] = selectCurrency.value

    let selectEmployment = document.getElementById("select-employment");
    data['employment'] = selectEmployment.value

    document.querySelectorAll('input[name="education"]').forEach(element => {
        data['education'] = '-'
        if (element.checked === true) {
            data['education'] = element.value
        }
    })

    document.querySelectorAll('input[name="show-on-page"]').forEach(element => {
        data['show_on_page'] = '-'
        if (element.checked === true) {
            data['show_on_page'] = element.value
        }
    })
    const params = new URLSearchParams(data);
    const response = await fetch("http://127.0.0.1:8000/api/filter_vacancies" + "?" + params);
}


document.querySelector('#searchBtn').addEventListener("click", getFilters)

document.querySelectorAll(".send-cv").forEach((element) => {
  element.addEventListener("click", showForm);
});

function showForm() {
  document.getElementById("myModal").style.display = "block";
}

function createModal (event) {
    myModalForm = document.querySelector('#send-response-form')
    myModalForm.action = `vacancy/${event.target.value}`
}

document.querySelectorAll(".send-cv").forEach(element =>  element.addEventListener("click", createModal))