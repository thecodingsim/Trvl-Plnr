// create an object that will store the functions, to use the API
let weather = {
    // you will need an apikey to access the weather. you can look over the documentation to see what the key is capable of getting. If you recieve an 'invalid apikey' error, it is still undergoing validation. 
    // error made: ***MAKE SURE that your apiKey is in quotations!!
    "apiKey": "b468e87c8d11bd446b35a797aec0deb1",
    // we will use the url to get information about the weather. First we will create a function with city as the parameter to look up any city
    fetchWeather: function (city) {
        // fetch will be given a url
        fetch(
            "https://api.openweathermap.org/data/2.5/weather?q=" 
            + city 
            + "&units=imperial&appid=" 
            + this.apiKey
        )
            // once the url is fetched, it will "do" a response to json
            .then((response) => response.json())
        // then we will log that data into the console. We should recieve information about the weather in the console (in the inspect tool)
            .then((data) => this.displayWeather(data))
    },
    // this will display the weather on the page, that will take in the data:
    displayWeather: function(data) {
        // this will extract 'name' from this object. You can look at your results data from the api key to gather this information:
        const { name } = data;
        // if the array contains the object, you can use index of 0 to get the first element of data.weather:
        const { icon, description } = data.weather[0];
        const { temp, humidity } = data.main;
        const { speed } = data.wind;
        // log this data into the console (inspect) to test:
        // console.log(name, icon, description, temp, humidity, speed)
        // display this information on the page:
        document.querySelector(".city").innerText = "Weather in " + name;
        // change all the other information:
        document.querySelector(".icon").src = "https://openweathermap.org/img/wn/" + icon + ".png";
        document.querySelector(".description").innerText = description;
        document.querySelector(".temp").innerText = temp + "°F";
        document.querySelector(".humidity").innerText = "Humidity: " + humidity + "%";
        document.querySelector(".wind").innerText = "Wind speed: " + speed + "km/h";
        // hide results while loading:
        document.querySelector(".weather").classList.remove("loading");
        // get images tied to specific cities, by replacing landscape with name:
        document.body.style.backgroundImage = "url('https://source.unsplash.com/1600x900/?" + name + "')"
    },
    // function to search for the weather:
    search: function () {
        this.fetchWeather(document.querySelector(".search-bar").value);
    }
};

// ==============search bar functions===================

// this will allow the user to use the search button when clicked
document.querySelector(".search button").addEventListener("click", function () {
    // we will call the function search
    weather.search();
});

// this will add an event for the input box so that when the user presses the enter key, it searches for the weather:
document.querySelector(".search-bar").addEventListener("keyup", function (event) {
    if (event.key == "Enter") {
        weather.search();
    }
})

// this will hide results from user while loading:
weather.fetchWeather("California");