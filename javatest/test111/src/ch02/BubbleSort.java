package ch02;

public class BubbleSort {

  public static void sort(long[] arr) {
    long tmp = 0;
    for (int i = 0; i < arr.length - 1; i++) {
      for (int j = arr.length - 1; j > i; j--) {
        System.out.println("i=" + i + "; j=" + j);
        if (arr[j] < arr[j - 1]) {
          //进行交换
          tmp = arr[j];
          arr[j] = arr[j - 1];
          arr[j - 1] = tmp;
        }
      }
    }
  }
}
