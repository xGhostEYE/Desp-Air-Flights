<script setup>
let showFlights = false;
let airports = ["Saskatoon", "Regina", "Calgary"];

</script>
 
<template>    
  <h1 class="fixed-top text-center">Desp-Air Flights</h1>
    <div class="container">
      <div class="navbar navbar-expand-lg fixed-top">
        <span class="h1">Desp-Air Flights</span>
      </div>
    <div class="row flex-nowrap">
      <!-- <nav class="col navbar navbar-light bg-light"> -->
        <div class="container-fluid">
          <span class="navbar-brand mb-0 h1">Navbar</span>
          <SearchComponent @getFlights="getFlights" :airports="airports" />
    </div>

<!--       </nav>
 -->      <div class="col">
        <ResultsComponent :class="{'invisible': !showFlights, 'col': true}" :results="results" />
      </div>
    </div>
  </div>

  <footer class="text-center text-white fixed-bottom" style="background-color: #f1f1f1;">
  <div class="text-center text-dark p-3" style="background-color: #214177;">
    © 2022 Copyright:
    <p class="text-dark" style="display:inline">Team_1 CMPT370-22-Fall University of Saskatchewan</p>
  </div>
  </footer>
</template>



<script>
import SearchComponent from './components/SearchComponent.vue';
import ResultsComponent from './components/ResultsComponent.vue';
import axios from 'axios';
import TitleComponent from './components/TitleComponent.vue';

export default {
  name: "App",
  components: {
    ResultsComponent,
    SearchComponent,
    TitleComponent
},
  data() {
    return {
      airports: ["Saskatoon", "Regina", "Calgary"],
      results: null,
      baseURL: "http://127.0.0.1:5000",
    };



  },
  mounted () {
    axios
      .get(this.baseURL + '/airports')
      .then(response => (this.airports = response.data));
  },
  methods: {
    async getFlights (dep, des) {
      this.showFlights = true;
      this.processResults(null);
      /* await axios
        .get(this.baseURL + '/flights', {
          params: {
            departure: String(dep),
            destination: String(des)
          }
        })
        .then(response => (this.processResults(response.data))); */

    },
    processResults(flightData) {
      //this.results = flightData;
      this.results = [{
  'flights': [
  {
    'departure': {
      'location': 'Saskatoon', 
      'time': '19:15',
      'airport code': 'YXE'
    },
    'arrival': {
      'location': 'Winnipeg', 
      'time': '21:53',
      'airport code': 'YWG'
    },
   'cost': 0, 
   'airline': 'WestJet',
   'flight number': 'WS3266'
},
{
  'departure': {
      'location': 'Saskatoon', 
      'time': '19:15',
      'airport code': 'YXE'
    },
    'arrival': {
      'location': 'Winnipeg', 
      'time': '21:53',
      'airport code': 'YWG'
    },
   'cost': 0, 
   'airline': 'WestJet',
   'flight number': 'WS3266',
   'startTime': '19:15',
   'endTime': '21:53'
}
],
'totalCost': '5',
'totalTime': '0:44',
'startTime':'19:15',
'endTime': '21:53'
}];
    }
  }
};
</script>



<style>
.p{
  margin-top: 0px;
}
.container{
  font-family: "Merienda", Helvetica, Arial;
  font-size: 20px;
}

</style>
