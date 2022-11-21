<script setup>
let showFlights = false;
let airports = ["Saskatoon", "Regina", "Calgary"];

</script>
 
<template>    

<div class="d-flex flex-column justify-content-center p-5">   
    <div class="border rounded-2 p-3" style="background-color: rgb(177, 199, 204); width:400px">
        <SearchComponent @getFlights="getFlights" :airports="airports" />
    </div>

    <div v-if="this.noFlights">
      <br>
        <div class="row gy-6" style="height:10px; width: 800px;">
          <div class="card w-75">
            <div class="card-body">
              <BIconExclamationCircle/>
              <h5 class="card-title">Sorry...</h5>
              <p class="card-text">No flights are available for that path at this time.</p>
            </div>
          </div>
        </div>
      </div>
      <div class="d-flex flex-column justify-content-center" v-else>
      <ResultsComponent :class="{'invisible': !showFlights, 'col': true}" :results="results" />
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
      results: [],
      baseURL: "http://127.0.0.1:5000",
      noFlights: false,
    };



  },
  mounted () {
    axios
      .get(this.baseURL + '/airports')
      .then(response => (this.airports = response.data));
  },
  methods: {
    async getFlights (dep, des) {
      
      this.processResults(null);
      /* await axios
        .get(this.baseURL + '/flights', {
          params: {
            departure: String(dep),
            destination: String(des)
          }
        })
        .then(response => (this.processResults(response.data))); */
        this.showFlights = this.results.length > 0;
        this.noFlights = this.results.length == 0;
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
'totalTime': '0:44h',
'startTime':'19:15',
'endTime': '21:53',
'url': 'https://www.google.com/search?q=monkeys&rlz=1C1CHBF_enCA921CA921&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiiiZDVgLv7AhWpIDQIHTibCLAQ_AUoAXoECAEQAw&biw=709&bih=903&dpr=1',
'isVisible':false
},
{
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
'totalCost': '$170',
'totalTime': '2:44h',
'startTime':'19:00',
'endTime': '21:44',
'url': 'https://www.google.com/search?q=monkeys&rlz=1C1CHBF_enCA921CA921&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiiiZDVgLv7AhWpIDQIHTibCLAQ_AUoAXoECAEQAw&biw=709&bih=903&dpr=1',
'isVisible':false
}]
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
