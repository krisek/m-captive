for i in (grep -Rle  hotspot *)                                                   
                              echo $i; perl -i.bak  -p -e 's/pi\/hotspot/pi\/m-captive/g;' "$i"                  
                          end

