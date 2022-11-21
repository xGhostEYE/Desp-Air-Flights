<script setup>
defineProps({
  results: {
    type: Object,
    required: true
  }
});
</script>



<template>
  <div class="d-flex flex-column m-5" style="height:10px; width: 750px;">
      <div class="accordion" id="accordionPanelsStayOpenExample">
        <ul style="padding: 50px">
        <li v-for="resultObject in this.results">
          <div class="accordion-item">
            <h2 class="accordion-header" id="panelsStayOpen-headingOne">
              <button class="accordion-button" type="button" @click="resultObject.isVisible = !resultObject.isVisible" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapseOne" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
                <div class="col-sm">
                  {{ resultObject.startTime }} - {{ resultObject.endTime }}
                </div>
                <div class="col-4">
                  {{ resultObject.totalTime }}
                </div>
                <div class="col-1">
                  {{ resultObject.totalCost }}
                </div>
              </button>
            </h2>
            <div id="panelsStayOpen-collapseOne" :class="resultObject.isVisible?'show': ''" class="accordion-collapse collapse" aria-labelledby="panelsStayOpen-headingOne">
              <div class="accordion-body content-align-center">
              <span v-for="item in resultObject.flights">
                  <span class="card-text">{{ item.departure.time }}   -    {{ item.departure.location }} ({{ item.departure['airport code'] }})</span>
                  <br/>
                  <BIconArrowDown/>
                  <br/>
                  <span class="card-text">{{ item.arrival.time }}   -    {{ item.arrival.location }} ({{ item.arrival['airport code'] }})</span>
                  <br/>
                  <br/>
                  <span class="card-text">{{ item.airline }}</span>
                  <br/>
                  <br/>
                  <button @click="redirectToFlight(resultObject.url)" class="btn btn-primary" style="background-color: #3E6D9C;">Take me to this flight!</button>
                  <hr/>
              </span>
              </div>
            </div>  
          </div>
        </li>
      </ul> 
      </div>
  </div>


</template>




<script>
export default {
  name: "Results",
  /* data() {
    return {
      
    };
  },*/
  methods: {
      redirectToFlight: function(url){
        window.open(url)
      } 
  }
};
</script>

<style>
 li {
    list-style-type: none;
    /* padding:50px; */
    left:-200px;
}

</style>