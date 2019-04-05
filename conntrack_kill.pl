#!/usr/bin/perl

open FILE, "/usr/sbin/conntrack -L |";
print "$ARGV[0]\n";

while($line = <FILE>){
    if($line =~ /$ARGV[0]/ && $line =~ /ESTAB/){
        
        %input = ();
        $line =~ s/(dport=\d+) .*/$1/;
        print "$line";
        @pairs = split(/\s+/, $line,8);
        foreach $item (@pairs) {
             ($key,$content)=split (/=/,$item,2);
             $content=~tr/+/ /;
             $content=~ s/%(..)/pack("c",hex($1))/ge;
             $input{$key}=$content if defined $content;
        }
        #foreach $key (keys %input){
        #    print "$key: $input{$key}\n";
        #    }
        #print "===\n";
        $cdrack = "conntrack -D --orig-src $input{src} --orig-dst $input{dst} -p tcp --orig-port-src $input{sport}  --orig-port-dst $input{dport}";
        print "$cdrack\n";
        open CDEL, "$cdrack |";
        while(<CDEL>){
            
            }
        close CDEL;
    }
}
close FILE;
#/usr/sbin/conntrack -L  |grep $1  |grep ESTAB  |grep 'dport=80'  |awk  "{ system("conntrack -D --orig-src $1 --orig-dst "  substr($6,5) " -p tcp --orig-port-src " substr($7,7) "  --orig-port-dst 80"); }"
