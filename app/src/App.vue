<script setup>
let showFlights = false;
let airports = [];

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
      path: {
        flights: [],
        totalCost: '$170',
        totalTime: '2:44',
        startTime:'19:00',
        endTime: '21:44',
        url: 'https://www.google.com/search?q=monkeys&rlz=1C1CHBF_enCA921CA921&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiiiZDVgLv7AhWpIDQIHTibCLAQ_AUoAXoECAEQAw&biw=709&bih=903&dpr=1',
        isVisible: false

      },
      airports: [],
      results: [],
      baseURL: "http://127.0.0.1:5000",
      noFlights: false,
    };



  },
  async mounted () {
    await axios
      .get(this.baseURL + '/airports')
      .then(response => {
        let i = 0;
        for (let i = 0;i<response.data.length;i++) {
          this.airports[i] = response.data[i][0] + " - " + response.data[i][1];
        }     
        
      });
  },
  methods: {
    async getFlights (dep, des) {
      
      //this.processResults(null);
      await axios
        .get(this.baseURL + '/flights', {
          params: {
            departure: String(dep.split(' - ')[1]),
            destination: String(des.split(' - ')[1])
          }
        })
        .then(response => (this.processResults(response.data)))
        .then(this.showFlights = true);

    },
    processResults(flightData) {
      //this.results = flightData;
      console.log(flightData);
      let tempResults = flightData;
      //loop through each path returned
      for (let pathI = 0;pathI<tempResults.length; pathI++) {
        let totalCost = 0;
        let firstDepartureTime = null;
        let finalArrivalTime = null;
        //loop through each flight in a path
        for (let flightI = 0; flightI<tempResults[pathI]['flights'].length;flightI++) {
          let startTime = new Date(tempResults[pathI]['flights'][flightI]['departure']['time'].replace(' ', ':'));
          let endTime = new Date(tempResults[pathI]['flights'][flightI]['arrival']['time'].replace(' ', ':'));
          //if this is the first flight, set the initial departure 
          if (flightI == 0) {
            firstDepartureTime = startTime;
          }
          // calculate the total cost
          if (tempResults[pathI]['flights'][flightI]['cost'] == null) {
            tempResults.splice(pathI, 1);
            pathI
            break;
          }
          totalCost += parseInt(tempResults[pathI]['flights'][flightI]['cost'].replace('$',''))
          //get the final arrival time date object
          finalArrivalTime = endTime;
          tempResults[pathI]['flights'][flightI]['arrival']['time'] = this.get12hrTimeString(endTime);
          tempResults[pathI]['flights'][flightI]['departure']['time'] = this.get12hrTimeString(startTime);
        }
        // set the results objects values
        tempResults[pathI]['startTime'] = this.get12hrTimeString(firstDepartureTime);
        tempResults[pathI]['startTimeSort'] = firstDepartureTime;
        tempResults[pathI]['endTime'] = this.get12hrTimeString(finalArrivalTime);
        tempResults[pathI]['endTimeSort'] = finalArrivalTime;
        tempResults[pathI]['cost'] = totalCost;
        tempResults[pathI]['totalTime'] = this.getTimeDifferenceString(finalArrivalTime, firstDepartureTime);
        tempResults[pathI]['totalTimeSort'] = finalArrivalTime - firstDepartureTime;
        tempResults[pathI]['isVisible'] = false;
      }
      this.results = tempResults;
      
// 'totalCost': '$170',
// 'totalTime': '2:44',
// 'startTime':'19:00',
// 'endTime': '21:44',
// 'url': 'https://www.google.com/search?q=monkeys&rlz=1C1CHBF_enCA921CA921&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiiiZDVgLv7AhWpIDQIHTibCLAQ_AUoAXoECAEQAw&biw=709&bih=903&dpr=1',
// 'isVisible':false
    },
    /**
     * gets the total time for the flight and returns it as a string in 
     */
    getTimeDifferenceString(finalArrivalTime, firstDepartureTime) {
      let duration = finalArrivalTime - firstDepartureTime;
      let minutes = Math.floor((duration / (1000 * 60)) % 60);
      let hours = Math.floor((duration / (1000 * 60 * 60)) % 24);
      
      return hours + " Hours and " + minutes + " Minutes";//this.get12hrTimeString(hours.toString() + ":" + minutes.toString());
    },
    /* converts time into 12-hr format string */
    get12hrTimeString(time) {
      let date = new Date(time);
      let hour = date.getHours();
      let minute = date.getMinutes();
      if (minute < 10) {
        minute = "0" + minute.toString();
      }
      let timeStr = hour.toString() + ":" + minute + "AM";
      if (hour>12) {
        timeStr = (hour-12).toString() + ":" + minute + "PM";
      }
      return timeStr;
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
</style>
