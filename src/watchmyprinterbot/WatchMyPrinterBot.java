/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package watchmyprinterbot;

import com.github.sarxos.webcam.Webcam;
import java.awt.Dimension;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.imageio.ImageIO;

/**
 *
 * @author javier
 */
public class WatchMyPrinterBot {

    public static void main(String[] args) throws IOException {
        List<Webcam> lista = new ArrayList();
        Webcam webcam;
        lista = Webcam.getWebcams();
        for (int i = 0; i < lista.size(); i++) {
            webcam = lista.get(i);
            System.out.println(webcam.getName());
        }

        webcam = lista.get(1);
        Dimension dimension = new Dimension(1280,720);
        Dimension dimensiones[] = new Dimension[1];
        dimensiones[0]=dimension;
        webcam.setCustomViewSizes(dimensiones);
        webcam.setViewSize(new Dimension (1280,720));
        webcam.open();
        BufferedImage image = webcam.getImage();

        ImageIO.write(image, "PNG", new File("test.png"));

    }

}
