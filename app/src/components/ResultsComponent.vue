<script setup>
defineProps({
  results: {
    type: Object,
    required: true
  }
});
</script>

<!-- non-hardcoded stuff
<template>
  <div class="column">
    <li v-for="resultObject in this.results">
      <div class="card w-200">  
        <span v-for="item in resultObject.flights">
          <div class="card-body">
            <h5 class="card-title">{{ item.startTime }} - {{ item.endTime }}    {{ item.totalTime }}   {{ item.totalStops }}    {{ item.totalCost }}</h5>

            <p class="card-text">{{ item.departure.time }} - {{ item.departure.location }} ({{ item.departure['airport code'] }})</p>

            <p class="card-text">{{ item.arrival.time }} - {{ item.arrival.location }} ({{ item.arrival['airport code'] }})</p>
            <p class="card-text">{{ item.airline }}</p>
            <a href="#" class="btn btn-primary">Take me to this flight!</a>
            <hr/>
          </div>
        </span>
      </div>
    </li>
  </div>  
</template>
-->

<template>
  <div class="column">
      <div class="card w-200">
          <div class="card-body">
            <h5 class="card-header">12:02 - 15:45 3h 43m 1 stop $345</h5>
            <!--<h5 class="card-title">12:02 - 15:45     3h 43m       1 stop       $345 </h5>-->

            <p class="card-text">12:02   -    Saskatoon (YXE)</p>

            <img src="node_modules/bootstrap-icons/icons/stop.svg" alt="">
            <div class="vr"></div>
            <img src="node_modules/bootstrap-icons/icons/stop.svg" alt="">
            
            <p class="card-text">13:12   -    Calgary (YYC)</p>
            <p class="card-text">Air Canada</p>
            <a href="#" class="btn btn-primary">Take me to this flight!</a>
            <hr>
            <p class="card-text">14:14   -    Calgary (YYC)</p>

            <img src="node_modules/bootstrap-icons/icons/stop.svg" alt="">
            <div class="vr"></div>
            <img src="node_modules/bootstrap-icons/icons/stop.svg" alt="">
            <p class="card-text">15:45   -    Vancouver (YVR)</p>
            <p class="card-text">WestJet</p>
            <a href="#" class="btn btn-primary">Take me to this flight!</a>
          </div>
      </div>
  </div>  
</template>

<script>
export default {
  name: "Results",
  /* data() {
    return {
      
    };
  } */
};
</script>