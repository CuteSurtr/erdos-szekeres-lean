# Base-R scientific figure. Inputs are the independently audited integer points.
# The plot illustrates exact certificates; floating-point rendering is not evidence.
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 1L)
out <- args[[1]]
P <- data.frame(i = 0:14,
  x = c(0,37,38,84,202,472,653,665,666,683,736,737,926,999,1000),
  y = c(0,-35,-248,-270,-640,-427,-757,-793,-717,-718,-567,-827,-895,-926,0))
A <- c(2,3,6,9)
K <- c(4,7,12,13)
line_at <- function(pair, x) {
  u <- match(pair[[1]], P$i); v <- match(pair[[2]], P$i)
  P$y[[u]] + (P$y[[v]] - P$y[[u]]) / (P$x[[v]] - P$x[[u]]) * (x-P$x[[u]])
}
orange <- '#B45309'; teal <- '#087E8B'; ink <- '#233044'; grey <- '#788291'
draw <- function() {
  par(mfrow=c(1,2), mar=c(4.6,4.6,4.2,1.3), oma=c(2.2,0,3.0,0),
      family='sans', fg=ink, col.axis=ink, col.lab=ink, cex=0.92)
  plot(P$x, P$y, type='n', xlim=c(-70,1080), ylim=c(-1010,80),
       xlab='x', ylab='y', main='A valid 15-point configuration', asp=1)
  polygon(P$x[P$i %in% K], P$y[P$i %in% K],
          border=teal, lwd=1.7, lty=2, col=adjustcolor(teal,0.045))
  points(P$x,P$y,pch=16,col=grey,cex=0.85)
  points(P$x[P$i %in% K],P$y[P$i %in% K],pch=1,col=teal,cex=1.4,lwd=1.7)
  points(P$x[P$i %in% A],P$y[P$i %in% A],pch=16,col=orange,cex=1.2)
  dx <- c(-20,12,-32,28,-22,0,-55,-40,-24,42,0,35,-24,20,20)
  dy <- c(24,25,15,-15,-25,30,0,-15,40,5,30,-27,-26,-35,24)
  segments(P$x,P$y,P$x+dx*.7,P$y+dy*.7,col=adjustcolor(grey,.45),lwd=.65)
  text(P$x+dx,P$y+dy,labels=P$i,cex=.82,
       col=ifelse(P$i %in% A,orange,ink))
  legend('bottomleft', c('Selected A = {2, 3, 6, 9}', 'Ambient four-cap {4, 7, 12, 13}'),
         pch=c(16,1), col=c(orange,teal), bty='n', cex=.76,
         pt.cex=c(1.1,1.25), inset=.01)
  x <- c(1000,1500)
  ell <- line_at(c(12,13),x); q36 <- line_at(c(3,6),x); q39 <- line_at(c(3,9),x)
  plot(x,ell,type='n',xlim=x,ylim=range(c(ell,q36,q39))+c(-35,45),
       xlab='X (to the right of every old point)',ylab='Terminal-line height',
       main='One ambient line protects both cap triples')
  abline(v=1000,col=grey,lty=3)
  lines(x,ell,col=teal,lwd=2.6)
  lines(x,q36,col=orange,lwd=2,lty=2)
  lines(x,q39,col=orange,lwd=2,lty=3)
  legend('bottomleft',c('Ambient tail (12, 13)', 'Selected tail (3, 6)', 'Selected tail (3, 9)'),
         col=c(teal,orange,orange),lty=c(1,2,3),lwd=c(2.6,2,2),bty='n',cex=.8)
  mtext('Terminal-safe selection fails; weaker protected selections still exist',
        side=3,outer=TRUE,line=.8,font=2,cex=1.15)
  mtext('Indices start at 0. Plotting is illustrative; the certificate uses exact integers and rational inequalities.',
        side=1,outer=TRUE,line=.55,cex=.77,col=grey)
}
dir.create(out,recursive=TRUE,showWarnings=FALSE)
svg(file.path(out,'terminal15.svg'),width=12.4,height=6.5,onefile=TRUE)
draw(); dev.off()
png(file.path(out,'terminal15.png'),width=1860,height=975,res=150,type='cairo')
draw(); dev.off()
write.csv(P,file.path(out,'plotted_points.csv'),row.names=FALSE)
