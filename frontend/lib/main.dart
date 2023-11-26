import "package:flutter/material.dart";
import "package:just_audio/just_audio.dart";

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Audio Streaming'),
        ),
        body: Center(
          child: ElevatedButton(
            onPressed: () {
              _playAudio();
            },
            child: const Text('Play Audio'),
          ),
        ),
        floatingActionButton: FloatingActionButton(
          onPressed: () {

          },
          child: const Icon(Icons.add),
        )
      ),
    );
  }

  void _playAudio() async {
    final player = AudioPlayer();
    await player.setUrl('http://localhost:8000/232');
    player.play();
  }
}