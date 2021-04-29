package datamining;

import java.util.*;

/**
 * project: Datamining
 *
 * @author dinar
 * @version v0.1
 */
public class Main {

    private final static int STREAM_LENGTH = 1_000_000;
    private final static int MAX_VALUE = 1000;

    private final static Random random = new Random();

    public static void main(String[] args) {
        goStream(STREAM_LENGTH, MAX_VALUE);
    }

    private static void goStream(int streamLength, int maxValue) {
        Map<Integer, Integer> items = new HashMap<>();
        List<Counter> random100Positions = generateValues(100, streamLength);
        List<Counter> random500Positions = generateValues(500, streamLength);

        for (int i = 0; i < streamLength; i++) {
            int randomItem = random.nextInt(maxValue);
            items.merge(randomItem, 1, Integer::sum);

            countAlonMatiasMoment(random100Positions, randomItem,i);
            countAlonMatiasMoment(random500Positions, randomItem, i);
        }

        findMoments(items);
        System.out.print("second moment for 100 is ");
        findAlanMoments(random100Positions, streamLength);
        System.out.print("second moment for 200 is ");
        findAlanMoments(random500Positions, streamLength);
    }

    private static void countAlonMatiasMoment(List<Counter> randomPositions, int item, int current) {
        randomPositions.forEach(counter -> {
            if (counter.getIndex() == current) {
                counter.setItem(item);
                counter.setCount(1);
            } else if (counter.getIndex() < current) {
                if (counter.getItem() == item) {
                    counter.setCount(counter.getCount() + 1);
                }
            }
        });
    }

    private static void findAlanMoments(List<Counter> list, int streamLength) {
        double result = list.stream()
                .map(counter -> streamLength * (counter.getCount()) * 2 - 1)
                .mapToInt(i -> i)
                .average()
                .getAsDouble();
        System.out.println(result);
    }


    private static List<Counter> generateValues(Integer count, Integer maxLength) {
        List<Counter> indexes = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            int index = random.nextInt(maxLength);
            Counter counter = new Counter();
            counter.setIndex(index);
            indexes.add(counter);
        }
        return indexes;
    }

    private static void findMoments(Map<Integer, Integer> items) {
        int zeroMoment = items.size();
        int firstMoment = items.keySet().stream()
                .mapToInt(items::get).sum();
        int secondMoment = items.keySet().stream()
                .mapToInt(items::get).map(i -> i * i)
                .sum();

        System.out.println("Zero moment is " + zeroMoment);
        System.out.println("First moment is " + firstMoment);
        System.out.println("Second moment is " + secondMoment);
    }
}

class Counter {

    private Integer item;

    private Integer index;

    private Integer count;

    public Integer getItem() {
        return item;
    }

    public void setItem(Integer item) {
        this.item = item;
    }

    public Integer getIndex() {
        return index;
    }

    public void setIndex(Integer index) {
        this.index = index;
    }

    public Integer getCount() {
        return count;
    }

    public void setCount(Integer count) {
        this.count = count;
    }
}
