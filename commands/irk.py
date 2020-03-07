def get_irk_community_guide(robot, bot, update):
    url = 'https://cafe.naver.com/ingressresistance'
    update.message.reply_text("레지스탕스를 선택하신 여러분 반갑습니다! "
                              "인그레스는 폰을 들고 실외로 나가서 포털을 직접 찾아 나서는 게임입니다. "
                              "기본적인 행동을 익히기 위해 먼저 오른쪽 상단 OPS의 트레이닝을 실행해 보세요. "
                              "네이버 카페 - 인그레스 레지스탕스 코리아에 가입하시면 초급가이드와 각종 꿀팁들을 보실 수 있습니다. "
                              "크고 작은 모임과 작전, 나이안틱 공식행사들에 참여하실 수 있는 기회도 있으니 꼭 한번 카페에 들러주세요.\n"
                              "%s" % url)