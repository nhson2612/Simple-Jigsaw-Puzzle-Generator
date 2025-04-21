package com.example.jigsawpuzzle;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.Random;

public class MaskGenerator {
    private final static int PUZZLE_SIZE = 566;  // hard code
    private final static int PIECE_SIZE = 100; // hard code
    private static final int TAB_SIZE = PIECE_SIZE / 3; // hard code
    private static final int MASK_SIZE = PIECE_SIZE + TAB_SIZE*2; // hard code
    private static final int PIECE_COUNT = 5; // hard code
    private static final Random RANDOM = new Random();


    public static void main(String[] args) throws IOException {
        BufferedImage originalImage = ImageIO.read(new File("C:\\Users\\Administrator.DESKTOP-98TGIBL\\Downloads\\input.png"));
        // grpc call to resize and pad
//        BufferedImage processedImage = invokeRPCMethod(originalImage,PUZZLE_SIZE,TAB_SIZE); // resize to 500x500px, TAB_SIZE is padding
        BufferedImage[] pieces = generatePuzzlePieces(originalImage);
    }

    private static BufferedImage[] generatePuzzlePieces(BufferedImage image) {
        BufferedImage[] jigsawPieces = new BufferedImage[PIECE_COUNT * PIECE_COUNT];

        int[][] topEdge = new int[PIECE_COUNT][PIECE_COUNT];
        int[][] rightEdge = new int[PIECE_COUNT][PIECE_COUNT];
        int[][] bottomEdge = new int[PIECE_COUNT][PIECE_COUNT];
        int[][] leftEdge = new int[PIECE_COUNT][PIECE_COUNT];

        for (int i = 0; i < PIECE_COUNT; i++) {
            for (int j = 0; j < PIECE_COUNT; j++) {
                // top
                if(i == 0){ // hàng đầu tiên
                    topEdge[i][j] = 0;
                }else {
                    topEdge[i][j] = -bottomEdge[i-1][j];
                }

                //left
                if(j == 0){ // cột đầu
                    leftEdge[i][j] = 0;
                }else {
                    leftEdge[i][j] = -rightEdge[i][j-1];
                }

                //bottom
                if (i == PIECE_COUNT - 1) { // hàng cuối
                    bottomEdge[i][j] = 0;
                } else {
                    bottomEdge[i][j] = RANDOM.nextBoolean() ? 1 : -1;
                }

                // right
                if (j == PIECE_COUNT - 1) { // cột cuối
                    rightEdge[i][j] = 0;
                } else {
                    rightEdge[i][j] = RANDOM.nextBoolean() ? 1 : -1;
                }
            }
        }
        for (int i = 0; i < PIECE_COUNT; i++) {
            for (int j = 0; j < PIECE_COUNT; j++) {
                int topLeftX = j * (PIECE_SIZE);
                int topLeftY = i * (PIECE_SIZE);
                System.out.println("Top : " + topEdge[i][j] +
                        " Right : " + rightEdge[i][j] +
                        " Bottom : " + bottomEdge[i][j] +
                        " Left : " + leftEdge[i][j] +
                        " Pixel (" + topLeftX +
                        "," + topLeftY);
                System.out.println();

//                jigsawPieces = createAndApplyMask(PIECE_SIZE,TAB_SIZE,topEdge[i][j],rightEdge[i][j],bottomEdge[i][j],leftEdge[i][j],
//                        topLeftX,topLeftY);
            }
        }
        return jigsawPieces;
    }
}
