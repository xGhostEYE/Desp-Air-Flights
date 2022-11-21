<script setup>
defineProps({
  airports: {
    type: Array,
    required: true
  }
});
</script>
<template>
  <div class="row gy-6 md-4">
    <div class="align-items-center justify-content-center">
        <label for="starting" class="form-label">Starting</label>
        <input class="form-control" list="startingList" name="starting" 
                id="starting" v-model="starting" 
                type="text" />
        <span id="startingErr" v-show="!this.validStarting"  class="form-text text-danger">Enter valid airport</span>
        <datalist id="startingList">
          <option v-for="airport in this.airports">{{airport}}</option>
        </datalist>
        <br/>
      
        <label id="destination label" for="destination" class="form-label">Destination</label>
        <input class="form-control" list="destinationList" name="destination" 
                id="destination" v-model="destination" />
        <span id="destinationErr" v-show="!this.validDestination" class="form-text text-danger">Enter valid airport</span>
        <datalist id="destinationList">
          <option v-for="airport in this.airports">{{airport}}</option>
        </datalist>
        <br/>
        <button :class="{'disabled': !this.validEntries()}" @click="search()" class="mt-1 btn btn-primary" style="background-color: #3E6D9C;">Search</button>
    </div>
  </div>  
</template>
<script>
export default {
    data() {
      return {
        starting: '',
        destination: '',
        visible1: true,
        validStarting: true,
        validDestination: true
      }
    },
    methods: {
      search(){
        this.validStarting = this.airports.includes(this.starting);
        if (this.validStarting)
          this.$emit('getFlights', this.starting, this.destination);
      },
      validEntries() {        
        return this.airports.includes(this.starting) && this.airports.includes(this.destination);
      },
      validateinput(value, validString) {
        if (value.length) {
          for (let airport of this.airports) {
            this[validString] = airport.toLowerCase().includes(value.toLowerCase());
            if (this[validString]) break;
          }
          this.validEntries();
        }
        else this[validString] = true;
      }
      
    },
    watch: {
      starting(value) {
        this.validateinput(value, "validStarting");
      },
      destination(value) {
        this.validateinput(value, "validDestination");
      },
    },
  };
</script>
