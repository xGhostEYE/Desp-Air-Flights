<script setup>
let showFlights = false;
let airports = ["Saskatoon", "Regina", "Calgary"];

</script>
 
<template>    
  
    <div class="container">
      <div class="navbar navbar-expand-lg fixed-top">
        <span class="h1">Desp-Air Flights</span>
      </div>
    <div class="row flex-nowrap">
      <div class="col-4 navbar navbar-light bg-light">
        <div class="d-flex flex-column align-items-center align-items-sm-start px-3 pt-2 min-vh-100">
      <!-- <nav class="col navbar navbar-light bg-light"> -->
        <div class="container-fluid">
          <span class="navbar-brand mb-0 h1">Navbar</span>
          <SearchComponent @getFlights="getFlights" :airports="airports" />
        </div>
        </div>
        </div>

<!--       </nav>
 -->      <div class="col-8">
        <ResultsComponent :class="{'invisible': !showFlights, 'col': true}" :results="results" />
      </div>
    </div>
  </div>
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
      baseURL: "http://127.0.0.1:5000"
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
      
      await axios
        .get(this.baseURL + '/flights', {
          params: {
            departure: String(dep),
            destination: String(des)
          }
        })
        .then(response => (this.processResults(response.data)));

    },
    processResults(flightData) {
      this.results = flightData;
    }
  }
};
</script>



<style>
.p{
  margin-top: 0px;
}
.title{
  background-color: #5F9DF7;
}
</style>
