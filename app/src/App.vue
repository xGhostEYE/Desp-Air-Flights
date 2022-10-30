<script>
export default{
  data() {
    return {
      title: 'Desp-Air Flights'
    }
  }
}

</script>




<template>
  <div class = "title display-1 fixed-top">
    <h1>{{title}}</h1>
  </div>
  <div class = "search_box ">
    <p class = "mb-0">Starting</p>
    <input
      :value="starting"
      @input="event => starting = event.target.value">
      <p class = "mt-5 mb-0">Destination</p>
    <input
      :value="destination"
      @input="event => destination = event.target.value">
      <div>
        <button class="mt-5 btn btn-info">Search</button>
      </div>
  </div>

 
</template>







<style>
.p{
  margin-top: 0px;
}
</style>
