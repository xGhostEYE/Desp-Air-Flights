<script setup>
let showFlights = false;
let airports = ["Saskatoon", "Regina", "Calgary"];

</script>
 
<template>    

  <div class="container">   
    <div class="row">
      <div class="container-fluid">
        <SearchComponent @getFlights="getFlights" :airports="airports" />
      </div>

    <div class="col">
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
'totalCost': '$255',
'totalTime': '0:44',
'startTime':'19:15',
'endTime': '21:53',
'url': 'https://www.google.com/search?q=monkeys&rlz=1C1CHBF_enCA921CA921&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiiiZDVgLv7AhWpIDQIHTibCLAQ_AUoAXoECAEQAw&biw=709&bih=903&dpr=1'
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
  margin-top: 50px;
}
.title{
  font-family: 'Kanit', sans-serif, 'Montserrat', sans-serif;
  font-size: 40px;
  color: black;

}
</style>
