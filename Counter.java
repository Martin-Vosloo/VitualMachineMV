public class Counter{
    private int cnt;

    public Counter(int i){
        cnt = i;
    }

    public int inc(){
        this.cnt++;

        return this.cnt -1;
    }
}