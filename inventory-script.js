//-------------------------FIREBASE CONFIG----------------------------

// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.9.2/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.9.2/firebase-analytics.js";

//import {readFileSync, promises as fsPromises} from 'fs';
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDHVBBKn17xeLD71ZWbJ_4Fp5hsvXAPCow",
  authDomain: "hep---dune.firebaseapp.com",
  databaseURL: "https://hep---dune-default-rtdb.firebaseio.com",
  projectId: "hep---dune",
  storageBucket: "hep---dune.appspot.com",
  messagingSenderId: "821178691057",
  appId: "1:821178691057:web:32be280f7c2bbc3bb32850",
  measurementId: "G-HP0CBW4REV"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

import { getDatabase, ref, child, onValue, get } from "https://www.gstatic.com/firebasejs/9.9.2/firebase-database.js";
const db = getDatabase();
const dbRef = ref(db);

console.log(db);

//----------------------------------------------------------------------------------

document.getElementById('submitSearchBtn').addEventListener("click", submitSearch);

var table = document.getElementById('dataTable');
var table_header = document.getElementById('tableHeader');
var table_body = document.getElementById('tableBody');
var caption = document.getElementById('tableCaption');
var cableSearch = document.getElementById('cable');
var mechSearch = document.getElementById('mech');
var barcodeSearch = document.getElementById('barcodeSearch');
var radio = document.getElementById('radioBtns');
var barcodeElement = document.getElementById('barcodeInput');
var barcode = barcodeElement.value;
var cable = {
  type: document.getElementById('cableType'),
  number: document.getElementById('cableNumber'),
  batch: document.getElementById('batchNumber'),
  barcode: barcodeElement
};
var mech = {
  part_desc: document.getElementById('partDescription'),
  line_num: document.getElementById('lineNumber'),
  barcode: barcodeElement
};

//GLOBAL VARIABLES FOR SUBMIT SEARCH METHOD
var path = '';
var whole_batch;
var label;
var itemName;

var rad = document.radioField.myRadios;
var prev = null;

for (var i = 0; i < rad.length; i++) {
    rad[i].addEventListener('change', function() {
        (prev) ? console.log(prev.value): null;
        //cable
        if (this.value == 1){
          mechSearch.style.visibility = 'hidden';
          cableSearch.style.visibility = 'visible';
        }
        //mechanical item
        else if (this.value == 2) {
          mechSearch.style.visibility = 'visible';
          cableSearch.style.visibility = 'hidden';
        }
        barcodeSearch.style.visibility = 'visible';
        if (this !== prev) {
            prev = this;
        }
        console.log(this.value)
    });
}
function toBottom()
{
    window.scrollTo(0, document.body.scrollHeight);
}

const csvData = 'Barcode Number,Line Item,Part Description,Part Number,Qty / Shipment,Distributor\n\
40000yyy001x,1,"M6-1x10MM, SBHC A2 SS SILVER PLATED",,156,Force Fasteners International\n\
40000yyy002x,2,CABLE CONTAINMENT BRACKET,SPPD-03-011,8,Van Cafe\n\
40000yyy003x,3,M5 X 52MM THREADED HEX STANDOFF VENTED,SPPD-03-012,20,\n\
40000yyy004x,4,M5X8MM SILVER PLATED SHCS,SCM-A2-05-008,40,\n\
40000yyy005x,5,M5 STAINLESS STEEL NORD-LOCK WASHER LARGE OD,NL5SPSS,56,\n\
40000yyy006x,6,M6X10MM BHCS SP,92095A224,4,\n\
40000yyy007x,7,M6 SCHNORR LOCK WASHER,B-SCHNORRM6,8,\n\
40000yyy008x,8,M5X12MM SILVER PLATED SHCS,SCM-A2-05-012,16,\n\
40000yyy009x,9,TEFLON WIRE GUIDE R1,SPPD-03-013,8,\n\
40000yyy010x,10,UPPER CABLES,,20,\n\
40000yyy011x,11,PASSTHROUGH CABLE,,20,\n\
40000yyy012x,12,PD GUIDE RAIL - FAR SIDE,SPPD-03-002,40,\n\
40000yyy013x,13,STAINLESS STEEL PD MOUNT ANGLE,SPPD-03-001,80,\n\
40000yyy014x,14,M3X10MM SILVER PLATED FSHCS,823008,160,\n\
40000yyy015x,15,M3 STAINLESS STEEL NORD-LOCK WASHER,NL3SS,160,\n\
40000yyy016x,16,M3 STAINLESS STEEL HEX NUT,HNMA2-03,160,\n\
40000yyy017x,17,M5X10MM SHCS SP,549050,160,\n\
40000yyy018x,18,M5 STAINLESS STEEL NORD-LOCK WASHER LARGE OD,NL5SPSS,160,\n\
40000yyy019x,19,PD GUIDE RAIL - READOUT SIDE,SPPD-03-007,40,\n\
40000yyy020x,20,STAINLESS PD MOUNT ANGLE,SPPD-03-001,80,\n\
40000yyy021x,21,M3X10MM SILVER PLATED FSHCS,823008,160,\n\
40000yyy022x,22,M3 STAINLESS STEEL NORD-LOCK WASHER,NL3SS,160,\n\
40000yyy023x,23,M3 STAINLESS STEEL HEX NUT,HNMA2-03,160,\n\
40000yyy024x,24,M5X16MM SILVER PLATED SHCS,SCM-A2-05-016,200,\n\
40000yyy025x,25,M5 STAINLESS STEEL NORD-LOCK WASHER LARGE OD,NL5SPSS,200,\n\
40000yyy026x,26,SASEBO BOARD,SPPD-03-005,20,\n\
40000yyy027x,27,G10 MOUNT PLATE,SPPD-03-004,20,\n\
40000yyy028x,28,SS MOUNT PLATE,SPPD-03-003,20,\n\
40000yyy029x,29,M6X10MM SILVER PLATED FSHCS,92125A234,20,\n\
40000yyy030x,30,CABLE HOUSING SHIM,SPPD-03-017,20,\n\
40000yyy031x,31,CABLE HOUSING CONSTRAINT,SPPD-03-016,20,\n\
40000yyy032x,32,CABLE STRESS RELIEF YOKE,SPPD-03-015,19,\n\
40000yyy033x,33,CABLE STRESS RELIEF YOKE TEMP SENSOR CONFIG,SPPD-03-015,1,\n\
40000yyy034x,34,M5X22MM SS BHSCS ,92095A482,80,\n\
40000yyy035x,35,M5 SCHNORR-LOCK WASHERS ,90898A027,80,\n\
40000yyy036x,36,"PLT1M-C76 CABLE TIE, AQUA BLUE, TEFZEL",,296,\n\
40000yyy037x,37,"PLT2S-C76 CABLE TIE, AQUA BLUE, TEFZEL",,156,\n\
40000yyy038x,38,"417900 M6, 6mm SS SAFETY WSHR (ALTERNATE: BELMETRIC WSH6SS)",,156,\n\
40000yyy039x,39,"M6-1x10MM, SBHC A2 SS SILVER PLATED",,80,\n\
40000yyy040x,40,SS BULKHEAD PLATE,SPPD-03-008,4,\n\
40000yyy041x,41,CABLE BULKHEAD ASSEMBLY,SPPD-03-014,4,\n\
40000yyy042x,42,M4 X 45MM THREADED HEX STANDOFF VENTED,SPPD-03-010,12,\n\
40000yyy043x,43,M4X12MM SILVER PLATED SHCS,SCM-A2-04-012,24,\n\
40000yyy044x,44,M4 STAINLESS STEEL NORD-LOCK WASHER LARGE OD ,NL4SPSS,24,\n\
40000yyy045x,45,M5X12MM SILVER PLATED SHCS,SCM-A2-05-012,16,\n\
40000yyy046x,46,M5 STAINLESS STEEL NORD-LOCK WASHER LARGE OD,NL5SPSS,16,\n\
40000yyy047x,47,PD GUIDE RAIL - FAR SIDE,SPPD-03-002,40,\n\
40000yyy048x,48,STAINLESS PD MOUNT ANGLE,SPPD-03-001,80,\n\
40000yyy049x,49,M3X10MM SILVER PLATED FSHCS,823008,160,\n\
40000yyy050x,50,M3 STAINLESS STEEL NORD-LOCK WASHER,NL3SS,160,\n\
40000yyy051x,51,M3 STAINLESS STEEL HEX NUT,HNMA2-03,160,\n\
40000yyy052x,52,M5X10MM SHCS SP,549050,160,\n\
40000yyy053x,53,M5 STAINLESS STEEL NORD-LOCK WASHER LARGE OD,NL5SPSS,160,\n\
40000yyy054x,54,PD GUIDE RAIL - READOUT SIDE,SPPD-03-007,40,\n\
40000yyy055x,55,STAINLESS PD MOUNT ANGLE,SPPD-03-001,80,\n\
40000yyy056x,56,M3X10MM SILVER PLATED FSHCS,823008,160,\n\
40000yyy057x,57,M3 STAINLESS STEEL NORD-LOCK WASHER,NL3SS,160,\n\
40000yyy058x,58,M3 STAINLESS STEEL HEX NUT,HNMA2-03,160,\n\
40000yyy059x,59,M5X16MM SILVER PLATED SHCS,SCM-A2-05-016,200,\n\
40000yyy060x,60,M5 STAINLESS STEEL NORD-LOCK WASHER LARGE OD,NL5SPSS,200,\n\
40000yyy061x,61,SASEBO BOARD,SPPD-03-005,20,\n\
40000yyy062x,62,G10 MOUNT PLATE,SPPD-03-004,20,\n\
40000yyy063x,63,SS MOUNT PLATE,SPPD-03-003,20,\n\
40000yyy064x,64,M6X10MM SILVER PLATED FSHCS,92125A234,20,\n\
40000yyy065x,65,CABLE HOUSING SHIM,SPPD-03-017,20,\n\
40000yyy066x,66,CABLE HOUSING CONSTRAINT,SPPD-03-016,20,\n\
40000yyy067x,67,CABLE STRESS RELIEF YOKE,SPPD-03-015,20,\n\
40000yyy068x,68,M5X22MM BHCS ,92095A482,80,\n\
40000yyy069x,69,M5 SCHNORR-LOCK WASHERS ,90898A027,80,\n\
40000yyy070x,70,"PLT1M-C76 CABLE TIE, AQUA BLUE, TEFZEL",,136,\n\
40000yyy071x,71,"PLT2S-C76 CABLE TIE, AQUA BLUE, TEFZEL",,80,\n\
40000yyy072x,72,"417900 M6, 6mm SS SAFETY WSHR (ALTERNATE: BELMETRIC WSH6SS)",,80,\n\
50000yyy901x,901,Female Hirose Connector,798-HR10A-10R-12S71,10,Mouser\n\
50000yyy902x,902,Male Hirose Connector,798-HR10A-10P-12P73,30,Mouser\n\
50000yyy903x,903,D-Sub Housing,517-10314-C200-00,20,Mouser\n\
50000yyy904x,904,D-Sub Connector,517-10114-3000PC,20,Mouser\n\
50000yyy905x,905,D-Sub PCB Header,517-10214-55G3PC,20,Mouser\n\
50000yyy906x,906,SASEBO PCB,,20,Univ of Michigan\n\
50000yyy907x,907,PCB Brass Pins,575-5920000150000030,280,Mouser\n\
50000yyy908x,908,PCB Pin Receptacle,575-9837015801427100,280,Mouser\n\
50000yyy909x,909,"3-8"" Heat Shrink",FP038K-100-ND,50,DigiKey\n\
50000yyy910x,910,"1-16"" Heat Shrink",517-301116BU/REEL,30,Mouser\n\
50000yyy911x,911,Cable,,495,\n'

//var fs = require("fs");
var barcode_table;
//const content = readFileSync("barcode.txt", 'utf-8');
barcode_table = csvData.split("\n").map(function(row){return row.split(",");});

console.log(barcode_table);


//let dataTable = Papa.parse(csvData, => {
//    complete: function(results) {
//		console.log("Finished:", results.data);
//	}
//});


var qc_order = ['Cut to Length', 'Labeled', 'Headers', 'Stripped', 'Connector', 'Prelim Test', 'Heat Shrink', 'Final Test', 'QC Verfied'];

function createQCArray(snapshot){
  let qc = [];
  for(let i = 0; i < qc_order.length; i++){
    snapshot.forEach((child) => {
      //console.log(child.key, child.val());
      if(child.key == qc_order[i]){
        qc.push([child.key,child.val().replace('--', '\n')]);
      }
    });
  }
  return qc;
}

function findValue(code){
  let entries = barcode_table;
  let line_num = code.substring(8,11);
  line_num = String(parseInt(line_num)); //gets rid of leading zeroes
  for(let i = 0; i < entries.length; i++){
    if(entries[i][1] == line_num){
      return entries[i][2];
    }
  }
}

var upperlens = ['6570', '0780', '1390', '2075', '2685', '3370', '3980', '4665', '5275', '5960'];
var lowerlens = ['6109', '0579', '1219', '1778', '2438', '2985', '3632', '4197', '4851', '5436'];
var passlen = '7850';
let length = '0';

function makeLabel(type, number, batch){
  let label = 'PD-';
  if(type == 'Passthroughs'){
    label += 'U-P-';
    length = passlen;
    console.log(length);
  }else if(type == 'Uppers'){
    label += 'U-R-';
    if(number != -1){
      length = upperlens[number];
    }
  }else if(type == 'Lowers'){
    label += 'L-R-';
    if(number != -1){
      length = lowerlens[number];
    }
  }
  if(number >= 0){
    if(number == 0){
      label += '1';
    }else{
      label += '0';
    }
  label += number + '-';
  }else{
    label += 'xx-'
    length = 'xxxx';
  }
  label += batch + '-';
  label += length;
  return label;
}

function findCableType(barcode){
  if(barcode.charAt(0) == 1){
    return 'Uppers';
  }
  if(barcode.charAt(0) == 2){
    return 'Lowers';
  }
  if(barcode.charAt(0) == 3){
    return 'Passthroughs';
  }else{
    return 'Cable Type Not Found';
  }
}
function findCableNumber(barcode){
  if(barcode.charAt(1) == 0){
    return '10';
  }else{
    return barcode.charAt(1);
  }
}
function findBatchNum(barcode){
  return barcode.substring(2,5);
}

function createCableTable(snapshot, whole_batch, label){
  let cap = document.createElement('caption');
  cap.innerHTML = label;
  table.appendChild(cap);

  if(whole_batch){
    //create QC table for an entire batch
    let headerRow = document.createElement('tr');
    let first_header = document.createElement('th');
    first_header.innerHTML = 'Cable Number:';
    headerRow.appendChild(first_header);
    for(let i = 0; i < qc_order.length; i++){
      let header = document.createElement('th');
      header.innerHTML = qc_order[i];
      headerRow.appendChild(header);
    }
    //table_header.appendChild(headerRow);
    table.appendChild(headerRow);

    for(let i = 1; i < 11; i++){
      let dataRow = document.createElement('tr');
      if(snapshot.child(i.toString()).exists()){
        let qc = createQCArray(snapshot.child(i.toString()));
        console.log('QC doc ' + i + ': ');
        console.log(qc);

        let data = document.createElement('td');
        data.innerHTML = i.toString();
        dataRow.appendChild(data);

        //iterate through each step corresponding to cable 'i'
        console.log('qc: ' + qc);
        qc.forEach((step) => {
          let data = document.createElement('td');
          data.innerHTML = step[1];
          console.log(dataRow);
          dataRow.appendChild(data);
        });
        table_body.appendChild(dataRow);

      }else{
        //current cable does not exist in the database
        console.log('Cable ' + i + ' does not exist in this batch');
      }
    }
    table.appendChild(table_body);
  }else{
    //create QC form for a single cable
    let qc = createQCArray(snapshot);
    let headerRow = document.createElement('tr');
    let dataRow = document.createElement('tr');

    //iterate through each qc step stored in a 2D createQCArray
    //where step[0] is the name of the step completed
    //and step[1] is the name and date of who completed the step
    qc.forEach((step) => {
      //create table cells
      let header = document.createElement('th');
      let data = document.createElement('td');

      //create the header row and add each step name 1 by 1
      header.innerHTML = step[0];
      headerRow.appendChild(header);

      //create the data row and add each QC signature 1 by 1
      data.innerHTML = step[1];
      dataRow.appendChild(data);


    });
    table_header.appendChild(headerRow);
    table_body.appendChild(dataRow);
    table.appendChild(table_header);
    table.appendChild(table_body);

  }
}
function createMechTable(snapshot, itemName){
  let cap = document.createElement('caption');
  cap.innerHTML = itemName;
  table.appendChild(cap);
  let tr1 = document.createElement('tr');
  let td1 = document.createElement('td');
  let td2 = document.createElement('td');
  console.log(snapshot);
  td1.innerHTML = Object.keys(snapshot)[0];
  td2.innerHTML = Object.values(snapshot)[0];
  tr1.appendChild(td1);
  tr1.appendChild(td2);
  table.appendChild(tr1);
}

function submitSearch(){
  toBottom();
  table.innerHTML = '';
  barcode = barcodeElement.value;
  label = '';
  path = '';
  whole_batch = false;
  itemName = '';
  console.log(barcode);
  if(prev.value == 1){
    //cable
    if(barcode.length > 0){
      //barcode was entered for cable
      let cable_type = findCableType(barcode);
      let cable_number = findCableNumber(barcode);
      let batch_number = findBatchNum(barcode);
      path = cable_type + '/Batch/' + batch_number + '/' + cable_number;
      label = makeLabel(cable_type, cable_number, batch_number);
    }else{
      //barcode was not entered for cable
      let cable_type = cable.type.value;
      let cable_number = cable.number;
      if(cable_number.value.toString() < 1){
        //cable number is -1 if not specified
        cable_number.value = -1;
        whole_batch = true;
        console.log('no cable number');
      }else{
        cable_number = cable_number.value;
      }
      let batch_number = cable.batch.value;
      path = cable_type + '/Batch/';
      label = makeLabel(cable_type, cable_number, batch_number);
      if(cable_type != 'Passthroughs' && cable_type != 'Lowers' && cable_type != 'Uppers'){
        alert('Cable type must be one of the following: Passthroughs, Uppers, Lowers.');
        throw new Error('Unacceptable Value Entered');
      }
      if(batch_number.length > 0){
        path += batch_number + '/';
      }else{
        alert('Must Enter a Batch Number!');
        throw new Error('Unacceptable Value Entered');
      }
      if(!whole_batch){
        path += cable_number;
      }
      console.log('Path: ' + path);
    }
    //NEED TO AUTHENTICATE OR CHANGE DB RULES FOR THIS TO WORK
    get(child(dbRef, path)).then((snapshot) => {
      console.log(path);
      if (snapshot.exists()) {
        console.log(snapshot.val());
        createCableTable(snapshot, whole_batch, label);
      }else{
        console.log('no data found');
      }
    }).catch((error) => {
      console.error(error);
    });

  }
  if(prev.value == 2){
    //mech
    if(barcode.length > 0){
      //barcode was entered
      itemName = findValue(barcode);
    }else{
      //barcode was not entered
      if(mech.part_desc.value.length > 0){
        //search by part description
        itemName = mech.part_desc.value;
      }else{
        //search by line number
        let code = '40000yyy0';
        if(mech.line_num.value > 100){
          code = '50000yyy'
        }
        else if(mech.line_num.value < 10){
            code += '0';
        }
        code += mech.line_num.value;
        code += 'x';

        itemName = findValue(code);
      }
      console.log('Item Name: ' + itemName);
    }
    get(child(dbRef, 'Mechanical/' + itemName)).then((snapshot) => {
      if(snapshot.exists()){
        console.log(snapshot.val());
        createMechTable(snapshot.val(), itemName);
      }else{
        console.log('no data available');
      }
    }).catch((error) => {
      console.error(error);
    });
  }
}
