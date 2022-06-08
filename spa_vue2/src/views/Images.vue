<template>
  <div class="text-center" >
    <!-- --------------------------------------------------------- -->
    <v-container class="mt-4 mb-0 pb-0">
      <v-row no-gutters>
        <v-col class="text-left" cols="8">
          <v-btn 
            dark
            small
            class="purple darken-3 mx-3"
            min-width="100"
            @click="dialogUpload = !dialogUpload"
            >Upload</v-btn>

          <v-btn 
            :disabled="data.length==0"
            dark
            small
            class="purple darken-3 mx-3"
            min-width="100"
            @click="selected_all_images"
            >select all</v-btn>

          <v-btn 
            :disabled="selectedImages.length==0"
            dark
            small
            class="purple darken-3 mx-3"
            min-width="100"
            @click="selectedImages=[]"
            >un-select</v-btn>
      
          <v-btn 
            :disabled="selectedImages.length==0"
            dark
            small
            class="purple darken-3 mx-3"
            min-width="100"
            @click="dialogDelete = !dialogDelete"
            >Delete</v-btn>
        </v-col>

        <v-col cols="2">
          <v-select
            :items="sortTypes"
            v-model="$store.state.images.sortSelected"
            label="Sort" 
            dense
            solo
            class="d-inline-flex mx-2"
            @change="sort_data"
          ></v-select>
        </v-col>
        <v-col class="text-right" cols="2">
          <v-select
            :items="viewItems"
            v-model="$store.state.images.viewSelected"
            label="View" 
            dense
            solo
            class="d-inline-flex mx-2"
          ></v-select>
        </v-col>
      </v-row>
    </v-container>

    <!-- --------------------------------------------------------- -->
    <ImagesThumbs 
      v-if="$store.state.images.viewSelected=='thumbs'"
      v-bind:data="data" 
      v-bind:switch_selected="switch_selected" 
      v-bind:is_selected="is_selected" 
    />

    <!-- ---------------------------- -->
    <ImagesTable 
      v-if="$store.state.images.viewSelected=='table'"
      v-bind:data="data" 
      v-bind:switch_selected="switch_selected" 
      v-bind:is_selected="is_selected" 
    />

    <!-- --------------------------------------------------------- -->
    <v-row
      v-if="this.mainLoader"
      class="fill-height mt-16 pt-16"
      align="center"
      justify="center"
    >
      <v-progress-circular
        indeterminate
        color="purple"
        size="120"
      ></v-progress-circular>
    </v-row>

    <!-- --------------------------------------------------------- -->
    <v-dialog
      v-model="dialogDelete"
      max-width="500px"
    >
      <v-card class="">
        <v-card-title class="purple darken-3 white--text mb-6">
          Delete selected ({{selectedImages.length}}) images?
        </v-card-title>

        <v-sheet class="ma-12" v-if="snapLoader">
          <v-row
            class="fill-height"
            align="center"
            justify="center"
          >
            <v-progress-circular
              indeterminate
              color="purple"
              size="80"
            ></v-progress-circular>
          </v-row>
        </v-sheet>

        <v-card-actions>
          <v-container class="text-center">
            <v-btn
              v-if="!snapLoader"
              dark 
              class="purple darken-3 mx-4" 
              min-width="120"
              type="submit"
              @click="submit_images_delete"
            >Ok</v-btn>
            <v-btn
              dark 
              class="grey darken-1 mx-4"
              min-width="120"
              type="button"
              @click="dialogDelete = !dialogDelete"
            >Close</v-btn>
          </v-container>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- -------------------------------------------------- -->
    <v-dialog
      v-model="dialogUpload"
      max-width="500px"
    >
      <v-card class="">
        <v-card-title class="purple darken-3 white--text mb-2">
          Upload Images
        </v-card-title>
        <v-card-text class="pt-6" v-if="!snapLoader">
          <v-file-input
            v-model="uploadList"
            small-chips
            multiple
            label="File input ( jpeg and png )"
            accept="image/png, image/jpeg"
          ></v-file-input>
        </v-card-text>

        <v-sheet class="ma-12" v-else>
          <v-row
            class="fill-height"
            align="center"
            justify="center"
          >
            <v-progress-circular
              indeterminate
              color="purple"
              size="80"
            ></v-progress-circular>
          </v-row>
        </v-sheet>

        <v-card-actions>
          <v-container class="text-center">
            <v-btn
              v-if="uploadList.length"
              dark 
              class="purple darken-3 mx-4" 
              min-width="120"
              @click="submit_upload_images"
            >Submit</v-btn>
            <v-btn
              dark 
              class="grey darken-2 mx-4"
              min-width="120"
              type="button"
              @click="dialogUpload = !dialogUpload; uploadList = []"
            >Close</v-btn>
          </v-container>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- --------------------------------------------------------- -->

  </div>
</template>


<script>
  import ImagesTable from '../components/ImagesTable'
  import ImagesThumbs from '../components/ImagesThumbs'
  import axios from 'axios'

  import { mapMutations } from 'vuex'

  export default {
    name: 'Images',
    components: {
      ImagesTable,
      ImagesThumbs,
    },
    data: () => ({
      title: "Images",
      // viewSelected: "thumbs",
      viewItems: [
        { 
          value: "thumbs",
          text: "Thumbs"
        },
        { 
          value: "table",
          text: "Table"
        }
      ],
      sortTypes: [
        { 
          text: "Filename (ASC)",
          value: ["filename", "asc"]
        },
        { 
          text: "Filename (DESC)",
          value: ["filename", "desc"]
        },
        { 
          text: "Image-Type",
          value: ["contentType"]
        },
        { 
          text: "Uploaded (ASC)",
          value: ["uploadDate", "asc"]
        },
        { 
          text: "Uploaded (DESC)",
          value: ["uploadDate", "desc"]
        }
      ],
      mainLoader: false,
      snapLoader: false,
      streamBase: "/api/stream/",
      data:[],
      streamReady:false,
      // streamTmpUrls:{},
      selectedImages: [],
      acts:[
        {
          title: "anything",
        },
        {
          title: "delete",
        }
      ],
      dialogUpload: false,
      uploadList: [],
      dialogDelete: false
    }),
    
    methods:{
      ...mapMutations([ "set_err", "reset_err" ]),

      //---------------------------------------------------
      call_thumbs(loader=false){
        if(loader) this.mainLoader = true
        axios.get( "/api/thumbs?b64_data=yes", this.$store.getters.create_bearer_auth_header)
        .then((res)=>{
          // console.log(res.data)
          this.data = res.data
        })
        .catch((err)=>{
          // console.log(err.message)
          this.set_err(err.message)
        })
        .finally(()=>{
          this.sort_data()
          this.mainLoader=false
        })
      },

      //---------------------------------------------------
      sort_data(){
        let sortAry = this.$store.state.images.sortSelected
        // console.log(sortAry)
        if(!sortAry) return
        if(sortAry[1] == "desc"){
          this.data.sort((b, a)=> a[sortAry[0]].localeCompare(b[sortAry[0]])) // !!!CRAZY!!!
        }
        else{
          this.data.sort((a, b)=> a[sortAry[0]].localeCompare(b[sortAry[0]])) // !!!CRAZY!!!
        }
        
      },
      
      //---------------------------------------------------
      is_selected(idx){
        if(this.selectedImages.includes(this.data[idx]._id)){
          return true
        }
        else return false
      },
      
      //---------------------------------------------------
      switch_selected(idx){
        if( this.selectedImages.includes(this.data[idx]._id) ){
          let delIdx = this.selectedImages.indexOf(this.data[idx]._id)
          this.selectedImages.splice(delIdx, 1)
        }
        else{
          this.selectedImages.push(this.data[idx]._id)
        }
      },

      //---------------------------------------------------
      selected_all_images(){
        this.selectedImages = []
        for(let idx in this.data){
          this.selectedImages.push(this.data[idx]._id)
        }
      },

      //---------------------------------------------------
      async submit_images_delete(){
        this.snapLoader = true
        let toRemove = {...this.selectedImages}
        for(let idx in toRemove){
          try{
            await axios.delete( "/api/image/"+toRemove[idx], this.$store.getters.create_bearer_auth_header)
          }
          catch(err){
            toRemove.splice(toRemove.indexOf(),1)
            this.set_err(err.message)
          } 
        }
        for(let idx in toRemove){
          await this.remove_image_item_by_id(toRemove[idx])
        }
        this.snapLoader = false
        this.dialogDelete = false
      },

      //---------------------------------------------------
      async remove_image_item_by_id(id){
        const item = this.data.find(thumb => thumb._id === id)
        this.data.splice(this.data.indexOf(item), 1)
        this.selectedImages.splice(this.selectedImages.indexOf(id), 1)
      },

      //---------------------------------------------------
      async submit_upload_images(){
        let tmpuploadList = {...this.uploadList}
        this.uploadList = []
        this.snapLoader = true

        // console.log(this.uploadList)
        const config = this.$store.getters.create_bearer_auth_header
        config.headers["Content-Type"] = "multipart/form-data"
        
        for(let idx in tmpuploadList){
          const formData = new FormData();
          formData.append("file", tmpuploadList[idx])
          try{
            await axios.post("/api/image", formData, config )
          }
          catch(err){
            this.set_err(err.message)
          }
        }

        this.snapLoader = false
        this.dialogUpload = false
        this.call_thumbs()
      }

      //---------------------------------------------------


      //---------------------------------------------------
      
    },
    mounted: function(){
      this.call_thumbs(true)
    }
    
  }
</script>




<style >
th{
  font-size: 14px !important;
}
td{
  /* background-color: transparent !important; */
  cursor: pointer !important;
}
.v-select{
  font-size: 14px;
  /* font-weight: bold; */
  /* text-transform: uppercase; */
}
</style>