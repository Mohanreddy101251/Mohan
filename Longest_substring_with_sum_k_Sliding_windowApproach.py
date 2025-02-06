# Sliding window
def longest_subArray(lstt,target):
    left=0
    max_length=0
    start,end=-1,-1
    sum=0
    
    for right in range(len(lstt)):
        sum +=lstt[right]
        
        while sum>target and left<=right:
            
            sum -=lstt[left]
            left +=1
            
        if sum==target:
            length=(right-left)+1
            
            if(length>max_length):
                max_length=length
                start,end=left+1,right+1
    return (start,end) if max_length>0 else ("","-1")
            
lstt=[16 ,13 ,24 ,9 ,21 ,48, 4, 9]
result=9
print(longest_subArray(lstt,result))
