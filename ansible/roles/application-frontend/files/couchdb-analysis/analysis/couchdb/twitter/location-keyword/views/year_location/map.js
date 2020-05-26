function (doc) {
    var date = doc.created_at;
    var date_array = date.split(" ");
    var year = date_array[date_array.length - 1];
    
    var location = doc.location;
    var state;
    if (location == "Melbourne") 
     { state = "VIC";}
    else if (location == "Adelaide")
      {state = "SA";}
    else if (location == "Brisbane")
      {state = "QLD";}
    else if (location == "Canberra")
      {state = "ACT";}
    else if (location == "Darwin")
      {state = "NT";}
    else if (location == "Hobart")
     { state = "TAS";}
    else if (location == "Perth")
     { state = "WA";}
    else if (location == "Sydney")
      {state = "NSW";}
    else if (location == "Victoria")
      {state = "VIC";}
    else if (location == "South Australia")
      {state = "SA";}
    else if (location == "Queensland")
      {state = "QLD";}
    else if (location == "New South Wales")
      {state = "NSW";}
    else if (location == "Northern Territory")
      {state = "NT";}
    else if (location == "Tasmania")
      {state = "TAS";}
    else if (location == "Western Australia")
      {state = "WA";}
    else
      {state = "OT"}
        
    emit([year, state], 1);
  }